# Task 3

The issue that could occur in the given DC-net is that two cryptographers send their name and timestamp at the same time. This would result in a broken encryption/decryption, since the assumption is that only one cryptographer sends data and the remaining one send empty strings.
If two cryptographers send their data the encryption/decryption results in nosense data which is also a way to determine the error. I.e. the data is decrypted malformed.

A possible solution is to resend the message radomly at later time