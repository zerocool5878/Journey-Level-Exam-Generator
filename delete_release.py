import requests

# Configuration
GITHUB_TOKEN = "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"
REPO_OWNER = "zerocool5878"
REPO_NAME = "Journey-Level-Exam-Generator"
VERSION = "v1.1.1"

def delete_release():
    """Delete a GitHub release"""
    # First get the release ID
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{VERSION}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"Getting release {VERSION}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        release_id = response.json()["id"]
        print(f"Found release ID: {release_id}")
        
        # Delete the release
        delete_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{release_id}"
        print(f"Deleting release...")
        delete_response = requests.delete(delete_url, headers=headers)
        
        if delete_response.status_code == 204:
            print(f"✅ Release {VERSION} deleted successfully!")
            
            # Also delete the tag
            tag_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/tags/{VERSION}"
            print(f"Deleting tag {VERSION}...")
            tag_response = requests.delete(tag_url, headers=headers)
            
            if tag_response.status_code == 204:
                print(f"✅ Tag {VERSION} deleted successfully!")
            else:
                print(f"⚠️ Failed to delete tag: {tag_response.status_code}")
        else:
            print(f"❌ Failed to delete release: {delete_response.status_code}")
            print(delete_response.json())
    else:
        print(f"❌ Failed to get release: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    delete_release()
