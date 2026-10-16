# OsintifyX - Instagram OSINT tool (profile, posts, engagement scraping)
# Original concept by MrHacker-X - https://github.com/MrHacker-X
# Upgraded: rich theme, single-pass scraping, error containment, safe file ops.

import os
import sys
import time
import shutil
import logging
from collections import Counter

import instaloader
from instaloader.exceptions import (
    InstaloaderException,
    LoginException,
    BadCredentialsException,
    TwoFactorAuthRequiredException,
    ConnectionException,
    ProfileNotExistsException,
)
from rich.console import Console
from rich.text import Text
from tabulate import tabulate

from config import usernamex, passwordx, OUTPUT_DIR, RATE_DELAY

logging.basicConfig(level=logging.WARNING)

console = Console(highlight=False)

ACCENT = "#7C4DFF"
GOLD   = "#FFC94A"
TEXT   = "grey93"
DIM    = "grey54"
ERROR  = "#FF5370"
WARN   = "#FFB86C"

loader = instaloader.Instaloader(
    quiet=True,
    compress_json=False,
    post_metadata_txt_pattern="",
    max_connection_attempts=3,
)

_post_cache = {}
t_username = ""
save_mode = False




def good_bye() -> None:
    print()
    console.rule(style=DIM)
    console.print(
        f"  [{GOLD}]◆[/] [{TEXT}]thanks for using [bold][{ACCENT}]OsintifyX[/][/]",
        highlight=False,
    )
    console.print(f"  [{DIM}]Network[/] [{ACCENT}]link.vritrasec.com[/]", highlight=False)
    console.print()
    print()


def _pause() -> None:
    try:
        input(f"\n  [{ACCENT}]◇[/] [{DIM}]press ENTER to continue[/] ")
    except (EOFError, KeyboardInterrupt):
        good_bye()
        sys.exit(0)
    print()


def _fail(e: Exception) -> None:
    name = type(e).__name__
    hint = "check target account (private/renamed?), login session, or wait out rate limits"
    console.print(
        f"\n  [{ERROR}]◆[/] [{ERROR}]scraping stopped[/] "
        f"[{DIM}]— {name}: {e}[/]",
        highlight=False,
    )
    console.print(f"  [{WARN}]◇[/] [{DIM}]hint: {hint}[/]", highlight=False)
    _post_cache.pop(t_username, None)
    print()


def _sleep() -> None:
    time.sleep(RATE_DELAY)


def get_profile(username: str):
    """Profile + posts fetched once per target, reused by every module."""
    return instaloader.Profile.from_username(loader.context, username)


def get_posts(profile) -> list:
    key = profile.username
    if key not in _post_cache:
        _sleep()
        _post_cache[key] = list(profile.get_posts())
    return _post_cache[key]


def show(body: list, table: str = None, save_name: str = None) -> None:
    print()
    console.print(Text("\n".join(body), style=TEXT), markup=False, highlight=False)
    if table:
        print()
        console.print(Text(table, style=TEXT), markup=False, highlight=False)
    if save_mode and save_name:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, save_name)
        text = "\n".join(body) + "\n\n" + (table or "")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        console.print(
            f"\n  [{GOLD}]◆ saved[/] [{DIM}]—[/] [{ACCENT}]{path}[/]",
            highlight=False,
        )


def m01_profile_info() -> None:
    profile = get_profile(t_username)
    posts = get_posts(profile)
    likes = comments = 0
    tagged = []
    hashtags = []
    for post in posts:
        likes += post.likes
        comments += post.comments
        tagged.extend(post.tagged_users)
        hashtags.extend(post.caption_hashtags)

    body = [
        f"[+] Profile Information of {t_username}:",
        "",
        f"[+] Username: {profile.username}",
        f"[+] Full Name: {profile.full_name}",
        f"[+] Biography: {profile.biography}",
        f"[+] Profile Picture URL: {profile.profile_pic_url}",
        f"[+] External URL: {profile.external_url}",
        f"[+] Followers: {profile.followers}",
        f"[+] Following: {profile.followees}",
        f"[+] Number of Posts: {profile.mediacount}",
        f"[+] Is Private Account: {profile.is_private}",
        f"[+] Is Verified Account: {profile.is_verified}",
        f"[+] Is Business Account: {profile.is_business_account}",
        f"[+] Business Category Name: {profile.business_category_name}",
        f"[+] Total Likes (all posts): {likes}",
        f"[+] Total Comments (all posts): {comments}",
        "",
        "[+] Top 5 Tagged Users:",
    ]
    for user, count in Counter(tagged).most_common(5):
        body.append(f"  @{user}: {count}")
    body.append("")
    body.append("[+] Top 5 Hashtags:")
    for tag, count in Counter(hashtags).most_common(5):
        body.append(f"  #{tag}: {count}")
    table = _table(
        [[i, u, c] for i, (u, c) in enumerate(Counter(tagged).most_common(), 1)],
        ["Index", "Tagged User", "Repeated"],
    )
    show(body, table, f"{t_username}_profile.txt")


def m02_hashtags() -> None:
    profile = get_profile(t_username)
    counts = Counter()
    for post in get_posts(profile):
        counts.update(post.caption_hashtags)
    rows = [[i, tag, c] for i, (tag, c) in enumerate(counts.most_common(), 1)]
    body = [f"[+] Hashtags of {t_username}: {len(counts)} unique across all posts"]
    table = _table(rows, ["Index", "Hashtags", "Repeated"])
    show(body, table, f"{t_username}_hashtags.txt")


def _account_table(entries) -> str:
    return _table(
        [[i, u.userid, u.username, u.full_name]
         for i, u in enumerate(entries, 1)],
        ["Index", "User ID", "Username", "Full Name"],
    )


def m03_followers() -> None:
    profile = get_profile(t_username)
    _sleep()
    followers = list(profile.get_followers())
    body = [f"[+] Followers of {t_username}: {len(followers)}"]
    show(body, _account_table(followers), f"{t_username}_followers.txt")


def m04_followings() -> None:
    profile = get_profile(t_username)
    _sleep()
    followees = list(profile.get_followees())
    body = [f"[+] Followings of {t_username}: {len(followees)}"]
    show(body, _account_table(followees), f"{t_username}_followings.txt")


def m05_tagged() -> None:
    profile = get_profile(t_username)
    counts = Counter()
    for post in get_posts(profile):
        counts.update(post.tagged_users)
    rows = [[i, u, c] for i, (u, c) in enumerate(counts.most_common(), 1)]
    body = [f"[+] Tagged users by {t_username}: {len(counts)} unique"]
    table = _table(rows, ["Index", "Tagged User", "Repeated"])
    show(body, table, f"{t_username}_tagged_users.txt")


def m06_post_details() -> None:
    profile = get_profile(t_username)
    body = []
    for post in get_posts(profile):
        body.append(f"[+] Post ID: {post.mediaid}")
        body.append(f"[+] Caption: {post.caption or ''}")
        body.append(f"[+] URL: {post.url}")
        body.append(f"[+] Likes: {post.likes} | Comments: {post.comments}")
        body.append(f"[+] Timestamp: {post.date_utc}")
        body.append(f"[+] Is Video: {post.is_video}")
        if post.is_video:
            body.append(f"[+] Video URL: {post.video_url}")
        tagged = ", ".join("@" + u for u in post.tagged_users) or "None"
        tags = ", ".join("#" + h for h in post.caption_hashtags) or "None"
        body.append(f"[+] Tagged Users: {tagged}")
        body.append(f"[+] Hashtags: {tags}")
        body.append("")
    show(body, None, f"{t_username}_post_details.txt")


def m07_captions() -> None:
    profile = get_profile(t_username)
    caps = [p.caption for p in get_posts(profile) if p.caption]
    rows = [[i, c] for i, c in enumerate(caps, 1)]
    table = _table(rows, ["Index", "Caption"])
    show([f"[+] Captions of {t_username}: {len(caps)}"], table,
         f"{t_username}_captions.txt")


def m08_locations() -> None:
    profile = get_profile(t_username)
    rows = []
    i = 1
    for post in get_posts(profile):
        if post.location:
            rows.append([i, post.location.name,
                         f"{post.location.lat}, {post.location.lng}"])
            i += 1
    table = _table(rows, ["Index", "Post Location", "Latitude, Longitude"])
    show([f"[+] Locations across {t_username}'s posts: {len(rows)}"], table,
         f"{t_username}_locations.txt")


def m09_stories() -> None:
    profile = get_profile(t_username)
    _sleep()
    target = os.path.join(OUTPUT_DIR, f"{t_username}_stories")
    if os.path.exists(target):
        shutil.rmtree(target)
    try:
        loader.download_stories(userids=[profile.userid])
    finally:
        if os.path.isdir(":stories"):
            shutil.move(":stories", target)
            console.print(
                f"  [{GOLD}]◆ done[/] [{DIM}]—[/] [{TEXT}]stories in [/]"
                f"[{ACCENT}]{target}[/]",
                highlight=False,
            )
        else:
            console.print(
                f"  [{WARN}]◇[/] [{TEXT}]no story found for {t_username}"
                f"[{DIM}] (nothing to download)[/]",
                highlight=False,
            )


def m10_profile_pic() -> None:
    _sleep()
    target = os.path.join(OUTPUT_DIR, f"{t_username}_profile_pic.jpg")
    try:
        loader.download_profile(t_username, profile_pic_only=True)
    finally:
        moved = False
        for jpg in glob.glob(os.path.join(t_username, "*.jpg")):
            if os.path.exists(target):
                os.remove(target)
            shutil.move(jpg, target)
            moved = True
        if os.path.isdir(t_username):
            shutil.rmtree(t_username)
        if moved:
            console.print(
                f"  [{GOLD}]◆ done[/] [{DIM}]—[/] [{TEXT}]profile pic: [/]"
                f"[{ACCENT}]{target}[/]",
                highlight=False,
            )
        else:
            console.print(
                f"  [{WARN}]◇[/] [{TEXT}]no profile picture received[/]",
                highlight=False,
            )


def m11_images() -> None:
    profile = get_profile(t_username)
    target = os.path.join(OUTPUT_DIR, f"{t_username}_photos")
    _sleep()
    n = 0
    for post in get_posts(profile):
        if post.is_video:
            continue
        loader.download_post(post, target=t_username)
        n += 1
    if os.path.isdir(t_username):
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.move(t_username, target)
        console.print(
            f"  [{GOLD}]◆ done[/] [{DIM}]—[/] [{TEXT}]{n} photo post(s) in [/]"
            f"[{ACCENT}]{target}[/]",
            highlight=False,
        )
    else:
        console.print(f"  [{WARN}]◇[/] [{TEXT}]no image posts found[/]", highlight=False)


def m12_commenters() -> None:
    profile = get_profile(t_username)
    counts = Counter()
    names = {}
    for post in get_posts(profile):
        for comment in post.get_comments():
            u = comment.owner.username
            counts[u] += 1
            names[u] = comment.owner.full_name
    rows = [[i, u, names[u], c] for i, (u, c) in enumerate(counts.most_common(), 1)]
    table = _table(rows, ["Index", "Username", "Full Name", "Comments"])
    show([f"[+] Commenters on {t_username}'s posts: {len(counts)} unique"], table,
         f"{t_username}_commenters.txt")


def m13_comments() -> None:
    profile = get_profile(t_username)
    body = []
    for post in get_posts(profile):
        for comment in post.get_comments():
            body.append(f"comment({comment.owner.username})> {comment.text}")
    show([f"[+] All comments on {t_username}'s posts: {len(body)}"],
         "\n".join(body) if body else "", f"{t_username}_comments.txt")


def m14_likers() -> None:
    profile = get_profile(t_username)
    for i, post in enumerate(get_posts(profile), 1):
        likers = list(post.get_likes())
        table = _table([[j, u.username, u.userid, u.full_name]
                        for j, u in enumerate(likers, 1)],
                       ["Index", "Username", "User ID", "Full Name"])
        show([f"[+] Post {i:02d} ({post.shortcode}) likers: {len(likers)}"],
             table, f"{t_username}_likers_post{i:02d}.txt")


def m15_bio() -> None:
    profile = get_profile(t_username)
    show([f"[+] Biography of {t_username}:", "", profile.biography],
         None, f"{t_username}_bio.txt")


def m16_media_types() -> None:
    profile = get_profile(t_username)
    types = {"GraphImage": "Image", "GraphVideo": "Video",
             "GraphSidecar": "Sidecar"}
    kinds = [types.get(p.typename, p.typename) for p in get_posts(profile)]
    total = len(kinds) or 1
    image, video, side = (kinds.count("Image"), kinds.count("Video"),
                          kinds.count("Sidecar"))
    body = [
        f"[+] Post types for {t_username}:",
        f"[+] Images: {image} [{image / total * 100:.2f}%]",
        f"[+] Videos: {video} [{video / total * 100:.2f}%]",
        f"[+] Sidecar: {side} [{side / total * 100:.2f}%]",
        f"[+] Total posts: {len(kinds)}",
    ]
    table = _table([[f"{i:02d}", t] for i, t in enumerate(kinds, 1)],
                   ["Index", "Post Type"])
    show(body, table, f"{t_username}_media_types.txt")


def about() -> None:
    body = [
        f"[+] About OsintifyX [{t_username}]:",
        "",
        "[+] Instagram OSINT tool: profile info, hashtags, followers/followings,",
        "[+] tagged users, post details, captions, locations, stories,",
        "[+] profile-pic and photo downloads, commenter/comment/liker stats,",
        "[+] biography, and media-type breakdown - 16 modules in one menu.",
        "",
        "[+] Data comes from the logged-in session in config.py and is saved",
        f"[+] locally in {OUTPUT_DIR}/ - nothing leaves your machine.",
        "",
        "[+] Use a disposable login account. Respect Instagram's terms and",
        "[+] the privacy of others. See TERMS.md before use.",
        "",
        "[+] Network: link.vritrasec.com",
    ]
    show(body, None, None)


menux = f"""
  [{DIM}]░▒▓[/] [{ACCENT}]Select any option to retrieve info[/] [{DIM}]░▒▓[/]

  [{GOLD}]◆[/] [bold][{ACCENT}]01-16[/][/] [{DIM}]scraping modules[/]
    [{TEXT}]01[/] Profile info      [{TEXT}]09[/] Stories
    [{TEXT}]02[/] Hashtags          [{TEXT}]10[/] Profile picture
    [{TEXT}]03[/] Followers         [{TEXT}]11[/] All images
    [{TEXT}]04[/] Followings        [{TEXT}]12[/] Commenter list
    [{TEXT}]05[/] Tagged users      [{TEXT}]13[/] All comments
    [{TEXT}]06[/] Post details      [{TEXT}]14[/] Likers per post
    [{TEXT}]07[/] Captions          [{TEXT}]15[/] Biography
    [{TEXT}]08[/] Locations         [{TEXT}]16[/] Media types

  [{GOLD}]◆[/] [bold][{ACCENT}]91[/][/] [{DIM}]About[/]   [{GOLD}]◆[/] [bold][{ACCENT}]95[/][/] [{DIM}]Network[/]   [{GOLD}]◆[/] [bold][{ACCENT}]99[/][/] [{DIM}]Exit[/]
"""


def network() -> None:
    console.rule(style=ACCENT)
    console.print(
        f"  [{GOLD}]◆[/] [{DIM}]Network[/] [{ACCENT}]link.vritrasec.com[/]",
        highlight=False,
    )
    console.rule(style=ACCENT)


dispatch = {
    "1": m01_profile_info, "01": m01_profile_info,
    "2": m02_hashtags, "02": m02_hashtags,
    "3": m03_followers, "03": m03_followers,
    "4": m04_followings, "04": m04_followings,
    "5": m05_tagged, "05": m05_tagged,
    "6": m06_post_details, "06": m06_post_details,
    "7": m07_captions, "07": m07_captions,
    "8": m08_locations, "08": m08_locations,
    "9": m09_stories, "09": m09_stories,
    "10": m10_profile_pic, "11": m11_images,
    "12": m12_commenters, "13": m13_comments, "14": m14_likers,
    "15": m15_bio, "16": m16_media_types,
}


def login() -> None:
    session_file = f"{usernamex}_session"
    if os.path.isfile(session_file):
        try:
            loader.load_session_from_file(usernamex, session_file)
            console.print(
                f"  [{GOLD}]◆[/] [{TEXT}]session restored[/] [{DIM}]({usernamex})[/]",
                highlight=False,
            )
            return
        except Exception:
            console.print(f"  [{WARN}]◇[/] [{DIM}]stale session - re-logging in[/]",
                          highlight=False)
    console.print(
        f"  [{GOLD}]◆[/] [{TEXT}]logging in as[/] [{GOLD}]{usernamex}[/]",
        highlight=False,
    )
    try:
        loader.login(usernamex, passwordx)
    except BadCredentialsException:
        console.print(
            f"  [{ERROR}]◆[/] [{ERROR}]wrong username or password[/] "
            f"[{DIM}]— fix usernamex / passwordx in config.py and retry[/]",
            highlight=False,
        )
        sys.exit(1)
    except TwoFactorAuthRequiredException:
        console.print(
            f"  [{ERROR}]◆[/] [{ERROR}]two-factor (2FA) login not supported[/] "
            f"[{DIM}]— use a disposable account without 2FA enabled[/]",
            highlight=False,
        )
        sys.exit(1)
    except LoginException as e:
        message = str(e)
        if "Checkpoint required" in message or "challenge" in message.lower():
            console.print(
                f"  [{ERROR}]◆[/] [{ERROR}]Instagram checkpoint on this account[/] "
                f"[{DIM}]— log into this account once in a browser, complete the "
                f"security check Instagram asks for, then run OsintifyX again[/]",
                highlight=False,
            )
        else:
            console.print(
                f"  [{ERROR}]◆[/] [{ERROR}]login refused by Instagram[/] "
                f"[{DIM}]— {message[:160]}[/]",
                highlight=False,
            )
        sys.exit(1)
    except ConnectionException as e:
        console.print(
            f"  [{ERROR}]◆[/] [{ERROR}]connection problem[/] [{DIM}]— check your "
            f"internet ({type(e).__name__})[/]",
            highlight=False,
        )
        sys.exit(1)
    except InstaloaderException as e:
        console.print(
            f"  [{ERROR}]◆[/] [{ERROR}]login failed[/] "
            f"[{DIM}]— {type(e).__name__}: {str(e)[:160]}[/]",
            highlight=False,
        )
        sys.exit(1)
    loader.save_session_to_file(session_file)
    console.print(f"  [{GOLD}]◆[/] [{TEXT}]logged in successfully[/]", highlight=False)


def pick_target() -> None:
    global t_username, _post_cache
    while True:
        try:
            t_username = console.input(
                f"[{GOLD}]◆[/] [bold][{ACCENT}]Target Username[/][/] [{DIM}]›[/] "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            good_bye()
            sys.exit(0)
        if not t_username:
            continue
        console.print(f"  [{DIM}]◇[/] [{TEXT}]checking username validity...[/]",
                      highlight=False)
        try:
            get_profile(t_username)
        except ProfileNotExistsException:
            console.print(f"  [{WARN}]◇[/] [{TEXT}]'{t_username}' does not exist "
                          f"[{DIM}]— try again[/]", highlight=False)
            continue
        except InstaloaderException as e:
            _fail(e)
            continue
        console.print(f"  [{GOLD}]◆[/] [{TEXT}]'{t_username}' is valid[/]",
                      highlight=False)
        _post_cache.clear()
        return


def pick_saving() -> None:
    global save_mode
    while True:
        try:
            answer = console.input(
                f"[{GOLD}]◆[/] [bold][{ACCENT}]Save results to {OUTPUT_DIR}/[/][/] "
                f"[{DIM}](y/n) ›[/] "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            good_bye()
            sys.exit(0)
        if answer in ("y", "yes"):
            save_mode = True
            return
        if answer in ("n", "no"):
            save_mode = False
            return
        console.print(f"  [{WARN}]◇[/] [{DIM}]answer with y or n[/]", highlight=False)


def module_run(fn) -> None:
    _sleep()
    try:
        fn()
    except InstaloaderException as e:
        _fail(e)
    except Exception as e:
        console.print(f"\n  [{ERROR}]◆[/] [{ERROR}]unexpected error[/] [{DIM}]— {e}[/]",
                      highlight=False)
        print()


def main() -> None:
    login()
    pick_target()
    pick_saving()
    while True:
        os.system("clear")
        if os.path.isfile("core/banr"):
            os.system("cat core/banr")
        console.print(banner_text(), highlight=False)
        console.print()
        try:
            choice = console.input(
                f"[{GOLD}]◆[/] [bold][{ACCENT}]Choose[/][/] [{DIM}]›[/] "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            good_bye()
            sys.exit(0)
        if choice == "":
            continue
        if choice in ("99", "exit", "bye"):
            good_bye()
            sys.exit(0)
        if choice in ("91",):
            os.system("clear")
            console.print()
            about()
            _pause()
            continue
        if choice in ("95",):
            network()
            _pause()
            continue
        fn = dispatch.get(choice)
        if fn is None:
            console.print(f"  [{WARN}]◇[/] [{DIM}]unknown option "
                          f"'{choice}' [/]", highlight=False)
            continue
        module_run(fn)
        _pause()


def banner_text() -> Text:
    return Text(
        f"  login {usernamex} · target {t_username} · saving "
        f"{'on' if save_mode else 'off'}",
        style=DIM,
    )


if __name__ == "__main__":
    from core.remote_control import RemoteControl

    with RemoteControl(tool_id="osintifyx"):
        try:
            main()
        except KeyboardInterrupt:
            good_bye()
            sys.exit(0)
