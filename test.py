import samino,time

vip = ["f63fc94e-324c-4181-b87f-c2a500a0b23b"] # userIds
client = samino.Client("22210FBEEEA9D9C77872C1D9E57892F6CE987064D3B9EA712461480F639FFD4AFC4B33191E466EDB9D")
client.login(email="heromr59@azel.xyz",password="Zezo1992",isWeb=True)


@client.event("on_message")
def on_message(data: samino.lib.Event):
	msg = data.message.content
	msgId = data.message.messageId
	comId = data.ndcId
	chatId = data.message.chatId
	userId = data.message.userId
	nickname = data.message.author.nickname
	try: mentionIds = data.message.json["extensions"]["mentionedArray"]
	except: pass
	local = samino.Local(comId)
	
	if msg.startswith("!tap") and chatId == "a1d77860-084e-40cf-855d-228d0fb333f2":
		local.send_message(chatId,"لقد حصلت على جائزتك اليومية",isWeb=True)
		for a in range(250): client.watch_ad(userId)
			
	if userId in vip:
		if msg.startswith("!follow"):
			for user in mentionIds:
				local.follow(user["uid"], isWeb=True)
				local.send_message(chatId, "تم متابعة العضو", isWeb=True)
	if msg.startswith("!unfollow"):
		for user in mentionIds:
			local.unfollow(user["uid"], isWeb=True)
			local.send_message(chatId, "تم إلغاء متابعة العضو", isWeb=True)

def socketRoot():
	while True:
		print("updating socket....")
		shundle = client.socket
		client.launch()
		shundle.luanch().close
		client.launch()
		print("updated socket!")
		time.sleep(300)
socketRoot()
