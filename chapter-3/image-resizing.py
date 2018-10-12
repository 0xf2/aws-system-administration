import tempfile
from PIL import Image
import shutil
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key

IMAGE_SIZES = [
    (250, 250),
    (125, 125)
]

bucket_name = sys.argv[1]
# Create a temporary directory to store local files
tmpdir = tempfile.mkdtemp()
conn = S3Connection()
bucket = conn.get_bucket(bucket_name)
for key in bucket.list(prefix='incoming/'):
    filename = key.key.strip('incoming/')
    print 'Resizing %s' % filename
    # Copy the file to a local temp file
    tmpfile = '%s/%s' % (tmpdir, filename)
    key.get_contents_to_filename(tmpfile)
    # Resize the image with PIL
    orig_image = Image.open(tmpfile)
    # Find the file extension and remove it from filename
    file_ext = filename.split('.')[-1]
    for resolution in IMAGE_SIZES:
        resized_name = '%s%sx%s.%s' % (filename.rstrip(file_ext), resolution[0], resolution[1], file_ext)
        print 'Creating %s' % resized_name
        resized_tmpfile = '%s/%s' % (tmpdir, resized_name)
        resized_image = orig_image.resize(resolution)
        resized_image.save(resized_tmpfile)
        # Copy the resized image to the S3 bucket
        resized_key = Key(bucket)
        resized_key.key = 'processed/%s' % resized_name
        resized_key.set_contents_from_filename(resized_tmpfile)
    # Delete the original file from the bucket
    key.delete()

# Delete the temp dir
shutil.rmtree(tmpdir)