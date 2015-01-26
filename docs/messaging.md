Just as it consumes messages from the Fedmsg bus, Fedimg emits messages of its
own.  The two message topics currently used are `image.upload` and
`image.test`. The modname for all Fedimg Fedmsgs is (appropriately) `fedimg`.

## image.upload

This message is utilized when the state of an image upload changes. This
message contains the following information:

-   `image_url`: the full address of the image file
-   `image_name`: the name of the image, created from the filename
-   `destination`: where the image will be uploaded to (includes region if
    applicable)
-   `status`: either 'started', 'completed', or 'failed'
-   `extra`: a dictionary that may contain service-specific information, such as an AMI ID for EC2

## image.test

This message is utilized when the state of an image test changes. This message
contains the following information:

-   `image_url`: the full address of the image file
-   `image_name`: the name of the image, created from the filename
-   `destination`: where the image has been uploaded to (includes region if
    applicable)
-   `status`: either 'started', 'completed', or 'failed'
-   `extra`: a dictionary that may contain service-specific information, such as an AMI ID for EC2
