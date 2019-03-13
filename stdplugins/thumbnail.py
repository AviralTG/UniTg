from telethon import events
from PIL import Image


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@borg.on(events.NewMessage(pattern=r"\.savethumbnail", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        downloaded_file_name = await borg.download_media(
            await event.get_reply_message(),
            Config.TMP_DOWNLOAD_DIRECTORY
        )
        end = datetime.now()
        ms = (end - start).seconds
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
        # resize image
        # ref: https://t.me/PyrogramChat/44663
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        img = Image.open(downloaded_file_name)
        # https://stackoverflow.com/a/37631799/4723940
        # img.thumbnail((90, 90))
        img.resize((90, height))
        img.save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await event.edit("Custom video / file thumbnail saved. This image will be used in the next upload.")
    else:
        await event.edit("Reply to a photo to save custom thumbnail")


@borg.on(events.NewMessage(pattern=r"\.clearthumbnail", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await event.edit("✅ Custom thumbnail cleared succesfully.")