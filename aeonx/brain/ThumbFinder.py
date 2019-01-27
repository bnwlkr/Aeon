#     # get account_id from Microsoft Azzure
#     def get_account_id(): 
#         url = "https://api.videoindexer.ai/auth/trial/Accounts"
#         response = requests.get(url)
#         
#         raw_data = json.loads(response.content.decode('utf-8'))
#         account_id = raw_data['id']
#         return account_id
#         
#     # get access token for a video
#     def get_video_token():
#         return []
# 
# 
#     # uploads a video, starts indexing and returns the video id
#     # require: account_id, account access token, video url
#     def video_upload(account_id, acount_token, path):
#         return []


def key_timestamps(account_id, video_id): 
    #account_id = "78782446-d6cf-4dab-81b5-30a90ade9a9f"
    #video_id = "56187c4f2e"
    url = "https://api.videoindexer.ai/trial/Accounts/"+account_id+"/Videos/"+video_id+"/Index?language=English"
    
    count = 0;              # total number of keyframes
    keyTimes = []           # array of timestamps
    
    response = requests.get(url)
    print(response.status_code)

    video_data = json.loads(response.content.decode('utf-8'))
    
    #print times of key frames
    shots = video_data['videos'][0]['insights']['shots']
    
    # number of shots in data, each shot contains a number of keyFrames
    num_shots = len(video_data['videos'][0]['insights']['shots'])
    
    for i in range(0,num_shots):
        for key in shots[i]: 
            if key == 'keyFrames':
                num_frames = len(shots[i]['keyFrames'])
                for j in range(0, num_frames): 
                    keyTimes.append(shots[i]['keyFrames'][j]['instances'][0]['adjustedStart'])
                    count = count + 1
    return keyTimes
    
