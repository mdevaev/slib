# -*- coding: utf-8 -*-


from slib import widgetlib


##### Public methods #####
@widgetlib.provides("tweet_button")
def tweetButton() :
	return ( """
			<a href="https://twitter.com/share" class="twitter-share-button" data-count="none">Tweet</a>
			<script>
			!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];
			if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";
			fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
			</script>
		""", )

