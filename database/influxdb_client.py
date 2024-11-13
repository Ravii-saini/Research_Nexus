from influxdb_client import InfluxDBClient, Point
from influxdb_client.rest import ApiException

# InfluxDB connection parameters
bucket = "research_data"
org = "IIT Guwahati"
token = "80TFSLaPPrO-jSWtDbl7pcOt1cI7S9E9cJmnEBhLdymbwNcKveDI9U6_p1az7BPyTBBKRL_a70eJA8i6y2n1Hw=="
url = "http://localhost:8086"

# Initialize InfluxDB client once
client = InfluxDBClient(url=url, token=token, org=org)

# Create write and query API once
write_api = client.write_api()
query_api = client.query_api()


def entry_exists(paper, topic):
    query = f'''
        from(bucket: "{bucket}")
        |> range(start: -1y)
        |> filter(fn: (r) => r["topic"] == "{topic}" and r["_field"] == "abstract" and r["_value"] == "{paper['abstract']}")
    '''
    query_api = client.query_api()
    result = query_api.query(query)
    
    return any(result)  # True if there's any record matching

def save_multiple_papers(papers, topic):
    for paper in papers:
        if "title" not in paper or "abstract" not in paper:
            print("Invalid paper data: Missing title or abstract")
            continue
        
        # Check for existing entry to avoid duplicates
        if entry_exists(paper, topic):
            print(f"Duplicate entry detected for '{paper['title']}'. Skipping save.")
            continue
        
        try:
            # Create the data point to be written into InfluxDB
            point = Point("research_paper")\
                    .tag("topic", topic)\
                    .field("abstract", paper["abstract"])
            
            # Write to the InfluxDB bucket
            write_api = client.write_api()
            write_api.write(bucket=bucket, org=org, record=point)
            print(f"Paper '{paper['title']}' saved successfully under topic '{topic}'")
        except ApiException as e:
            print(f"Error saving paper data to InfluxDB: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# def save_paper_data_batch(papers):
#     try:
#         points = [Point("research_paper").tag("topic", paper["title"]).field("abstract", paper["abstract"]) for paper in papers]
#         write_api.write(bucket=bucket, org=org, record=points)
#     except Exception as e:
#         print(f"Error saving paper data: {e}")

def get_paper_data(topic):
    try:
        # Construct the InfluxDB query with a time range filter
        query = f'''
            from(bucket: "{bucket}")
            |> range(start: -1y)
            |> filter(fn: (r) => r["topic"] == "{topic}")
        '''
        
        # Execute the query
        query_api = client.query_api()
        tables = query_api.query(query)
        
        papers = []
        seen_abstracts = set()  # To keep track of abstracts we've already added
        for table in tables:
            for record in table.records:
                abstract = record.get_value()
                if abstract not in seen_abstracts:  # Check if this abstract was already added
                    papers.append({
                        "title": record["topic"],  # Retrieve the 'topic' tag
                        "abstract": abstract  # Retrieve the value of 'abstract' field
                    })
                    seen_abstracts.add(abstract)  # Mark this abstract as seen
        
        if not papers:
            print(f"No papers found for topic: {topic}")
        
        return papers
    
    except ApiException as e:
        print(f"Error retrieving paper data from InfluxDB: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def close_influxdb_client():
    client.close()  # Close client connection when done
