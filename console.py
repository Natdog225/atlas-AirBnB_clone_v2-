#!/usr/bin/python3
"""This module defines the entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex
import re
import json
import ast
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance of a class, saves it (to the JSON file) and prints the id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in ["User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return False
        instance = eval(args[0])()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        try:
            obj_cls_str, obj_id = args[0], args[1]
            obj_cls = eval(obj_cls_str)
            storage = storage.all()
            obj_key = f"{obj_cls_str}.{obj_id}"
            if obj_key not in storage:
                print("** no instance found **")
                return
            obj = storage[obj_key]
            print(str(obj))
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (save the change into the JSON file)."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in ["User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        try:
            obj_cls_str, obj_id = args[0], args[1]
            obj_cls = eval(obj_cls_str)
            storage = storage.all()
            obj_key = f"{obj_cls_str}.{obj_id}"
            if obj_key not in storage:
                print("** no instance found **")
                return
            del storage[obj_key]
            storage.save()
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name."""
        args = shlex.split(arg)
        objects = storage.all()
        if len(args) > 0 and args[0] not in ["User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return False
        elif len(args) > 0:
            print([str(obj) for obj in objects.values() if type(obj).__name__ == args[0]])
        else:
            print([str(obj) for obj in objects.values()])

    def default(self, arg):
        """Default behavior for unknown commands"""
        try:
            func_name, args = arg.split('.', 1)
            if func_name in ['create', 'show', 'destroy']:
                getattr(self, f'do_{func_name}')(args)
            else:
                raise AttributeError
        except ValueError:
            print(f"*** Unknown syntax: {arg}")
        except AttributeError:
            print(f"*** Unknown command: {arg}")

def try_parse(json_str):
    try:
        return ast.literal_eval(json_str)
    except ValueError:
        return json_str

if __name__ == '__main__':
    HBNBCommand().cmdloop()
