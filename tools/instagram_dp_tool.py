import instaloader
import os
import requests # For direct download of profile pic URL

def download_insta_dp(username, output_path):
    L = instaloader.Instaloader()

    # Consider logging in for private profiles or to avoid rate limits.
    # Example: L.load_session_from_file("your_username", "path_to_session_file")
    # If no session file, user must login once:
    # try:
    #     L.load_session_from_file("your_username", "your_username.session")
    # except FileNotFoundError:
    #     username_inst = input("Enter your Instagram username for login: ")
    #     password_inst = input("Enter your Instagram password: ")
    #     L.login(username_inst, password_inst)
    #     L.save_session_to_file("your_username")

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        profile_pic_url = profile.profile_pic_url

        # Download using requests for more control over filename
        response = requests.get(profile_pic_url, stream=True)
        response.raise_for_status() # Raise an HTTPError for bad responses

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Optional: Verify file size or content if you want to be extra robust
        if os.path.getsize(output_path) < 1000: # Very small file might indicate an error page
            raise ValueError("Downloaded file is too small, possibly an error page instead of a DP.")

    except instaloader.exceptions.ProfileNotExistsException:
        raise ValueError(f"Instagram profile '{username}' does not exist.")
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        raise ValueError(f"Profile '{username}' is private and you are not following them.")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error while downloading DP: {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}. Check username or try logging in.")