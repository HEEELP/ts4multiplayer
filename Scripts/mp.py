from update import output


try:

    import distributor
    import server.client as client
    import omega
    import injector
    import pickle
    import zone
    import time
    import services, glob, sims4, inspect, re
    from server_commands.interaction_commands import has_choices, generate_choices, generate_phone_choices,  select_choice, cancel_mixer_interaction, cancel_super_interaction, push_interaction
    from server_commands.clock_commands import set_speed
    from server_commands.sim_commands import set_active_sim
    from decorator import decorator
    from undecorated import undecorated


    incoming_commands = []
    outgoing_commands = []

    class Message:
        def __init__(self, msg_id, msg):
            self.msg_id = msg_id
            self.msg = msg
            
    msg_count = 0
    is_client = False
    try:
        open("C:/Users/theoj/Documents/Electronic Arts/The Sims 4/Mods/Heuristics/Scripts/client", "rb")
        is_client = True
        
    except Exception:
        pass
    # @injector.inject_to(zone.Zone, "on_loading_screen_animation_finished")
    # def on_loading_screen_animation_finished(original, self):
        # original(self)
    files = glob.glob("C:/Users/theoj/Documents/Electronic Arts/The Sims 4/Mods/Heuristics/Scripts/delicious pickles/*.*")
    file_count = len(files)
    msg_count = file_count
    test_msg_count = 0
    def send_message_server(self, msg_id, msg):
        global msg_count
        global test_msg_count
        global outgoing_commands
        # output('id', str(self.id))
        if self.active:
                omega.send(self.id, msg_id, msg.SerializeToString())
                message = Message(msg_id, msg.SerializeToString())
                pickled_message = pickle.dumps(message)
                outgoing_commands.append(pickled_message)
                msg_count += 1
             
                
    def send_message_client(self, msg_id, msg):
        pass
        # don't actually send any commands at all from the original client's server



    last_synced_message_for_client = 0
    files = glob.glob("C:/Users/theoj/Documents/Electronic Arts/The Sims 4/Mods/Heuristics/Scripts/delicious pickles/*.*")
    file_count = len(files)
    last_synced_message_for_client = file_count
    def client_sync():
        global last_synced_message_for_client
        client_instance = services.client_manager().get_first_client()

        files = glob.glob("C:/Users/theoj/Documents/Electronic Arts/The Sims 4/Mods/Heuristics/Scripts/delicious pickles/*.*")
        file_count = len(files)

        for message_no in range(last_synced_message_for_client, file_count):
            msg_data = open("C:/Users/theoj/Documents/Electronic Arts/The Sims 4/Mods/Heuristics/Scripts/delicious pickles/{}.pkl".format(message_no), 'rb')
            unpacked_msg_data = pickle.load(msg_data)
            omega.send(client_instance.id, unpacked_msg_data.msg_id, unpacked_msg_data.msg)
                
        last_synced_message_for_client = file_count
        
    last_synced_command_for_server = 0

    def parse_arg(arg):
        new_arg = arg
        orig_arg = new_arg.replace('"', "").replace("(", "").replace(")", "").replace("'", "").replace(" ", "")
        new_arg = orig_arg
        try:
            new_arg = float(orig_arg)

            try: 
                new_arg = int(orig_arg)
            except BaseException:
                pass 
        except BaseException:
            pass 
        output("arg_handler", str(new_arg) + "\n")

        return new_arg
    command_count = 1
    regex = re.compile('[a-zA-Z]')

    command_names = ['interactions.has_choices',
                                          'interactions.choices',
                                          'interactions.phone_choices',
                                          'interactions.select',
                                          'interactions.cancel',
                                          'interactions.cancel_si',
                                          'interactions.push',
                                          'clock.setspeed',
                                          'sims.set_active']
               
                                          
    functions= [has_choices,
                        generate_choices,
                        generate_phone_choices,
                        select_choice,
                        cancel_mixer_interaction,
                        cancel_super_interaction,
                        push_interaction,
                        set_speed, 
                        set_active_sim]

               
    function_names = ["has_choices",
                        "generate_choices",
                        "generate_phone_choices",
                        "select_choice",
                        "cancel_mixer_interaction",
                        "cancel_super_interaction",
                        "push_interaction",
                        "set_speed",
                        "set_active_sim"]


    def server_update():
        global last_synced_command_for_server
        global command_count
        client_instance = services.client_manager().get_first_client()

        commands_to_be_processed = open("C:/Sandbox/Theo/DefaultBox/user/current/Documents/Electronic Arts/The Sims 4/Mods/Heuristics/Scripts/command_log.txt" , 'r')
        commands_to_be_processed = commands_to_be_processed.read()
        commands_to_be_processed = commands_to_be_processed.split('\n')

        for command in commands_to_be_processed[command_count : len(commands_to_be_processed)]:
            current_line = command.split(',')
            function_name = current_line[0]
            if function_name == '':
                continue
            parsed_args = []
            # output('arg_handler', str(current_line) + "\n")

            command_count += 1
            for arg_index in range(1, len(current_line)):
                arg = current_line[arg_index].replace(')', '').replace('{}', '').replace('(', '')
                if "'" not in arg:
                    arg = regex.sub('', arg)
                    arg = arg.replace('<._ = ', '').replace('>', '')
                parsed_arg = parse_arg(arg)
                parsed_args.append(parsed_arg)
            # output('arg_handler', "{}".format(function_name))
                
            function_to_execute = "{}({})".format(function_name, str(parsed_args).replace('[', '').replace(']',''))
            output('arg_handler', str(function_to_execute) + "\n" )
            exec(function_to_execute)



    @decorator
    def wrapper(func, *args, **kwargs):
        output("command_log",  "\n" + str(func.__name__) + ", " + str(args) +  "  " + str(kwargs))
        def do_nothing():
            pass
        # return func(*args, **kwargs)
        return do_nothing



    # def server_process():
        # global last_synced_message_for_client
        # last_synced_message_for_server = 1s
        
    def on_tick_client():
        try:
            client = services.client_manager().get_first_client()
            if client == None:
                return
        except Exception:
            return
        client_sync()

    def on_tick_server():
        try:
            client = services.client_manager().get_first_client()
            if client == None:
                return
            output("outgoing_commands",  str(len(outgoing_commands)) + "\n")
        except Exception:
            return
        server_update()
        
        
    import multiplayer_server

    if is_client:
        sims4.core_services.on_tick = on_tick_client
        client.Client.send_message = send_message_client
        for index in range(len(command_names)):
            functions[index] = sims4.commands.Command(command_names[index], command_type=sims4.commands.CommandType.Live)(wrapper(undecorated(functions[index])))
            
    else:
        client.Client.send_message = send_message_server
        sims4.core_services.on_tick = on_tick_server
        server_instance = multiplayer_server.Server()
        server_instance.listen(incoming_commands)
        server_instance.send()

    @sims4.commands.Command('get_con', command_type=sims4.commands.CommandType.Live)
    def get_con(_connection=None):
        output = sims4.commands.CheatOutput(_connection) 
        output(str(_connection))
        
        
    @sims4.commands.Command('checkid', command_type=sims4.commands.CommandType.Live)
    def checkid (_connection=None):
        # obj = object_manager.get(object_id)
        for obj in list(services.object_manager().objects):
            output('obj', str(obj) + " " + str(obj.id) +"\n")
            
    @sims4.commands.Command('shutdown', command_type=sims4.commands.CommandType.Live)
    def shutdown_server(_connection=None):
        # obj = object_manager.get(object_id)
        server_instance.shutdown(socket.SHUT_RDWR)
        server_instance.close()
except Exception as e:
    output("errors", str(e))