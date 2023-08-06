# Motion Master Protobuf API

This package contains generated Python code for the Synapticon Motion Master
Protobuf API.

Motion Master v3.x is supported. This package does not support previous versions.

## Installation

Using virtualenv or Python3's venv is recommended.

To install from PyPi, run

    $ pip install motion-master-proto

## Documentation

The only class of interest is the `MotionMasterMessage`.

    from motion_master_proto.motion_master_pb2 import MotionMasterMessage

    # Create a new message
    message = MotionMasterMessage()
    # Set the message type to 'get_system_version'
    message.request.get_system_version.SetInParent()

The `message` object can now be sent to the Motion Master on the DEALER socket.

For a full description of all messages, see the associated
`motion-master.proto` file.

## See also

Install the `motion-master-bindings` for easy access to the Synapticon Motion
Master.
