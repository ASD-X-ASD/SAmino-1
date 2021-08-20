import samino,time,os,sys
import wikipedia 
vip = ["f63fc94e-324c-4181-b87f-c2a500a0b23b"] # userIds
client = samino.Client("22C47F6E327764942738F7636FE42FB247FC9E4629C98C96D91CC1456D25FD07A153995C82213E4AC0")
client.login(email="heromr59@azel.xyz",password="Zezo1992",isWeb=True)

wikipedia.set_lang('ar')

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
		local.send_message(chatId,f"{nickname} لقد حصلت على جائزتك اليومية",asWeb=True)
		for a in range(300): client.watch_ad(userId)

	if msg.startswith("!join"):
		url=msg[6:]
		cId=client.get_from_link(url).objectId
		local.join_chat(cId,asWeb=True)
		msg="[C] تم الانضمام الي الدردشة !"
		local.send_message(chatId=chatId, message=msg,asWeb=True)
	if msg.startswith("!search"): st = wikipedia.search(msg[8:]);s = wikipedia.summary(st[0]);local.send_message(chatId=chatId, message=f"""
[BC]{st[0]}  
  
[C]{s[0:1500]}""",asWeb=True)
	if userId in vip:
		if msg.startswith("!follow"):
			for user in mentionIds:
				local.follow(user["uid"], isWeb=True)
				local.send_message(chatId, "تم متابعة العضو", asWeb=True)
	if msg.startswith("!unfollow"):
		for user in mentionIds:
			local.unfollow(user["uid"], isWeb=True)
			local.send_message(chatId, "تم إلغاء متابعة العضو", asWeb=True)

def socketRoot():
	while True:
		print("updating socket....")
		client.launch()
		shundle = client.socket;shundle.close();client.launch()
		time.sleep(300)
		sys.argv;sys.executable;print("restart now")
		os.execv(sys.executable, ['python'] + sys.argv)
socketRoot()
