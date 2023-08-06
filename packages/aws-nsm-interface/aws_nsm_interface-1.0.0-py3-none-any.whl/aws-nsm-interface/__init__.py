"""Main NSM interface module."""

# Standard library imports
import ctypes
import fcntl

# Related third party imports
import cbor2
from ioctl_opt import IOC, IOC_READ, IOC_WRITE

NSM_DEV_FILE = '/dev/nsm'
NSM_IOCTL_MAGIC = 0x0A
NSM_IOCTL_NUMBER = 0x00
NSM_REQUEST_MAX_SIZE = 0x1000
NSM_RESPONSE_MAX_SIZE = 0x3000

class IoVec(ctypes.Structure):
    """
    IoVec struct for use in the NsmMessage struct.

    The IoVec struct has two fields: iov_base, which is a pointer to a buffer,
    and iov_len, which defines the length of the contents in the buffer.

    The IoVec is used both to send data to /dev/nsm (in which case the length
    of the buffer is defined by the sender) and to receive data from /dev/nsm
    (in which case the length is set by /dev/nsm).
    """

    iov_base = None
    iov_len = None

    _fields_ = [
        ('iov_base', ctypes.c_void_p),
        ('iov_len', ctypes.c_size_t)
    ]

class NsmMessage(ctypes.Structure):
    """
    NsmMessage struct to interface with /dev/nsm.

    The NsmMessage struct has two fields: request, which contains the data
    sent to /dev/nsm, and response, which contains the data returned by /dev/nsm
    after the call has completed.
    """

    request = None
    response = None

    _fields_ = [
        ('request', IoVec),
        ('response', IoVec)
    ]

def self_test() -> None:
    """Run a self test."""
    file_handle = open_nsm_device()
    random = get_random(file_handle)
    close_nsm_device(file_handle)
    print(random)

def open_nsm_device() -> int:
    """Open the /dev/nsm file and return the file handle."""
    return open(NSM_DEV_FILE, 'w')

def close_nsm_device(file_handle: int) -> None:
    """Close the /dev/nsm file."""
    file_handle.close()

def get_random(file_handle: int, length: int = 32) -> bytes:
    """Request random bytes from /dev/nsm."""
    nsm_key = 'GetRandom'

    # Prepare a new NsmMessage with the given key.
    nsm_message = _new_nsm_message(nsm_key)

    # Send this message to /dev/nsm through an ioctl call.
    # When the call is complete, the response field of the
    # nsm_message will be filled with response data.
    _execute_ioctl(file_handle, nsm_message)

    # Read the binary reponse from NSM and convert it to a
    # Python dict.
    decoded_response = _decode_response(nsm_message)
    print(decoded_response)
    return decoded_response.get('random')

def _decode_response(nsm_message: NsmMessage) -> dict:
    """Read the binary reponse from NSM and return it as a Python dict."""
    # Create a buffer with a size as defined in the IoVec.iov_len field.
    cbor_data = bytearray(nsm_message.response.iov_len)

    # Create a pointer to this buffer.
    cbor_data_pointer = (ctypes.c_char * nsm_message.response.iov_len).from_buffer(cbor_data)

    # Copy the data referenced to by the IoVec into this buffer.
    ctypes.memmove(
        cbor_data_pointer,
        nsm_message.response.iov_base,
        nsm_message.response.iov_len
    )

    # Decode the CBOR and return it.
    return cbor2.loads(cbor_data)

def _execute_ioctl(file_handle: int, nsm_message: NsmMessage) -> None:
    """Send an NsmMessage to /dev/nsm trough ioctl."""
    # Calculate the IOWR operation. Should always result in 3223325184.
    operation = IOC(
        IOC_READ|IOC_WRITE,
        NSM_IOCTL_MAGIC,
        NSM_IOCTL_NUMBER,
        ctypes.sizeof(NsmMessage)
    )
    fcntl.ioctl(file_handle, operation, nsm_message)

def _new_nsm_message(key: str, data: dict = None) -> NsmMessage:
    """Generate a new NsmMessage struct for a request."""
    # Convert the key to Concise Binary Object Representation (CBOR).
    request_data = cbor2.dumps(key)
    request_data_len = len(request_data)

    # Create a buffer for the CBOR data and write the contents to it.
    request_data_buffer = (request_data_len * ctypes.c_uint8)(*request_data)

    # Create a pointer to the request buffer.
    request_data_pointer = ctypes.cast(
        ctypes.byref(request_data_buffer),
        ctypes.c_void_p
    )

    # Create a buffer to receive the response from /dev/nsm.
    # Make it as large as possible (NSM_RESPONSE_MAX_SIZE).
    response_buffer = (NSM_RESPONSE_MAX_SIZE * ctypes.c_uint8)()

    # Create a pointer to the response buffer.
    response_buffer_pointer = ctypes.cast(
        ctypes.byref(response_buffer),
        ctypes.c_void_p
    )

    # Initialize a new, empty NsmMessage struct.
    nsm_message = NsmMessage()

    # Create a new IoVec pointing to the request buffer. Assign the
    # IoVec to the request field of the NsmMessage.
    nsm_message.request = IoVec(
        request_data_pointer,
        request_data_len
    )

    # Create a new IoVec pointing to the response buffer. Assign the
    # IoVec to the response field of the NsmMessage.
    nsm_message.response = IoVec(
        response_buffer_pointer,
        NSM_RESPONSE_MAX_SIZE
    )

    return nsm_message
