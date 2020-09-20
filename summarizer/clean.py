from nltk.tokenize import word_tokenize

class DocClean:

    def _clean(self, line):
        line = line.strip().replace("newline_char", " ")
        line = line.replace("NEWLINE_CHAR", "")
        line = line.replace("( opens in new window )", "")
        line = line.replace("click to email this to a friend", "")
        line = line.replace("lick to share on whatsapp", "")
        line = line.replace("click to share on facebook", "")
        line = line.replace("share on facebook", "")
        line = line.replace("click to share on twitter", "")
        line = line.replace("click to share on pinterest", "")
        line = line.replace("click to share on tumblr", "")
        line = line.replace("click to share on google+", "")
        line = line.replace("feel free to share these resources in your social "
                            "media networks , websites and other platforms", "")
        line = line.replace("share share tweet link", "")
        line = line.replace("e-mail article print share", "")
        line = line.replace("read or share this story :", "")
        line = line.replace("share the map view in e-mail by clicking the share "
                            "button and copying the link url .     embed the map "
                            "on your website or blog by getting a snippet of html "
                            "code from the share button .     if you wish to "
                            "provide feedback or comments on the map , or if "
                            "you are aware of map layers or other "
                            "datasets that you would like to see included on our maps , "
                            "please submit them for our evaluation using this this form .", "")
        line = line.replace("share this article share tweet post email", "")
        line = line.replace("skip in skip x embed x share close", "")
        line = line.replace("share tweet pin email", "")
        line = line.replace("share on twitter", "")
        line = line.replace("feel free to weigh-in yourself , via"
                            "the comments section . and while you ’ "
                            "re here , why don ’ t you sign up to "
                            "follow us on twitter us on twitter .", "")
        line = line.replace("follow us on facebook , twitter , instagram and youtube", "")
        line = line.replace("follow us on twitter", "")
        line = line.replace("follow us on facebook", "")
        line = line.replace("play facebook twitter google plus embed", "")
        line = line.replace("play facebook twitter embed", "")
        line = line.replace("enlarge icon pinterest icon close icon", "")
        line = line.replace("follow on twitter", "")
        line = line.replace("autoplay autoplay copy this code to your website or blog", "")
        return line

    def clean_data(self, data, total_words=None):
        self.data = data
        self.total_words = total_words
        for idx, row in self.data.iterrows():
            try:
                text_newspaper = word_tokenize(row.content)
                if len(text_newspaper) >= self.total_words and self.total_words is not None:
                    text_newspaper = text_newspaper[:self.total_words]
                row.content = self._clean(" ".join(text_newspaper))
                self.data.loc[idx,'content_cleaned'] = row.content.lower()
            except:
                print(f"error with {idx}")
                self.data.loc[idx, 'content_cleaned'] = []
        return self.data

