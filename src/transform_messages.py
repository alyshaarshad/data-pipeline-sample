import datetime

def transform_message(json_data):
    # Extract necessary fields from the JSON data
    if json_data["type"] == "pull-requests":
        
        title = json_data.get("title", "")
        user = json_data.get("user", "")
        repository_name = json_data["repository"].get("name", "")
        repository_owner = json_data["repository"].get("owner", "")
        
        # Check if the values are None before converting to int
        created_at_str = json_data.get("created_at", "")
        created_at = datetime.datetime.utcfromtimestamp(int(created_at_str)) if created_at_str else None
        
        merged_at_str = json_data.get("merged_at", "")
        merged_at = datetime.datetime.utcfromtimestamp(int(merged_at_str)) if merged_at_str else None
        
        tags = "|".join([tag["name"] for tag in json_data["tags"]])
        state = json_data.get("status", "")
        body = json_data.get("body", "")
        
        return {"title": title, "user": user, "repository_name": repository_name, 
                "repository_owner": repository_owner, "created_at": created_at,
                "merged_at": merged_at, "tags": tags, "state": state, "body": body}
    
    elif json_data["type"] == "issue":
        
        title = json_data.get("title", "")
        user = json_data.get("user", "")
        repository_name = json_data["repository"].rsplit('/', 1)[-1]
        repository_owner = json_data["repository"].rsplit('/', 2)[-2]
        
        started_at_str = json_data.get("started_at", "")
        started_at = datetime.datetime.strptime(started_at_str, '%Y-%m-%dT%H:%M:%SZ') if started_at_str else None
        
        closed_at_str = json_data.get("closed_at", "")
        closed_at = datetime.datetime.strptime(closed_at_str, '%Y-%m-%dT%H:%M:%SZ') if closed_at_str else None
        
        labels = "|".join([label["name"] for label in json_data["labels"]])
        state = json_data.get("state", "")
        body = json_data.get("body", "")
        
        return {"title": title, "user": user, "repository_name": repository_name, 
                "repository_owner": repository_owner, "created_at": started_at,
                "merged_at": closed_at, "tags": labels, "state": state, "body": body}
    
    else:
        raise ValueError("Invalid message type")
    
