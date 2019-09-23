import paralleldots
import csv



paralleldots.set_api_key("LWJJJpTs3Shws6TSBhmKFTFGEDAuxqu6AqLKGsD5Ybk")

with open('comments.csv','r+') as csv_file:
    csv_read=csv.DictReader(csv_file, delimiter=',')
    line_count=0
    text=""
    for row in csv_read:
            text=text.strip()+row["Comment".strip()]
            line_count=line_count+1


print("\n==========================")
print(line_count,"comments processed",end="")
print("\n==========================\n")
sentiments=paralleldots.sentiment( text )
s=sentiments['sentiment']
emotions=paralleldots.emotion( text )
e=emotions['emotion']
if line_count > 0:
        print("Analyzed absolute sentiments:")
        print(f"Negative: {s['negative']}\nNeutral: {s['neutral']}\nPositive: {s['positive']}\n")
        
        print("Analyzed absolute:") 
        print(f"Angry: {e['Angry']}")
        print(f"Happy: {e['Happy']}")
        print(f"Excited: {e['Excited']}")
        print(f"Fear: {e['Fear']}")
        print(f"Sad: {e['Sad']}")
        print(f"Bored: {e['Bored']}\n")
        
else:
    print("No comments recieved error :(\n")