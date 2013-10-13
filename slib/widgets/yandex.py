# -*- coding: utf-8 -*-


import ulib.validators.common

from slib import widgetlib


##### Public constants #####
YA_SHARE_SERVICES_LIST = (
	"yaru",
	"vkontakte",
	"facebook",
	"twitter",
	"odnoklassniki",
	"moimir",
	"lj",
	"friendfeed",
	"moikrug",
	"gplus",
	"pinterest",
	"surfingbird",
)


##### Public methods #####
@widgetlib.provides("ya_metrika_informer")
def metrikaInformer(site_id) :
	site_id = ulib.validators.common.validNumber(site_id, 0)
	informer = ( """
			<!-- Yandex.Metrika informer -->
			<a href="http://metrika.yandex.ru/stat/?id=%(site_id)d&amp;from=informer"
			target="_blank" rel="nofollow"><img src="//bs.yandex.ru/informer/%(site_id)d/3_1_FFFFFFFF_EFEFEFFF_0_pageviews"
			style="width:88px; height:31px; border:0;" alt="Яндекс.Метрика" title="Яндекс.Метрика: данные за сегодня (просмотры, визиты и уникальные посетители)"
			onclick="try{Ya.Metrika.informer({i:this,id:%(site_id)d,type:0,lang:'ru'});return false}catch(e){}"/></a>
			<!-- /Yandex.Metrika informer -->
		""" % { "site_id" : site_id } )
	return (informer,)

@widgetlib.provides("ya_metrika_counter")
def metrikaCounter(site_id) :
	site_id = ulib.validators.common.validNumber(site_id, 0)
	counter = ( """
			<!-- Yandex.Metrika counter -->
			<script type="text/javascript">
			(function (d, w, c) {
				(w[c] = w[c] || []).push(function() {
					try {
						w.yaCounter%(site_id)d = new Ya.Metrika({id:%(site_id)d, enableAll: true});
					} catch(e) { }
				});

				var n = d.getElementsByTagName("script")[0],
					s = d.createElement("script"),
					f = function () { n.parentNode.insertBefore(s, n); };
				s.type = "text/javascript";
				s.async = true;
				s.src = (d.location.protocol == "https:" ? "https:" : "http:") + "//mc.yandex.ru/metrika/watch.js";

				if (w.opera == "[object Opera]") {
					d.addEventListener("DOMContentLoaded", f);
				} else { f(); }
			})(document, window, "yandex_metrika_callbacks");
			</script>
			<noscript><div><img src="//mc.yandex.ru/watch/%(site_id)d" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
			<!-- /Yandex.Metrika counter -->
		""" % { "site_id" : site_id } )
	return (counter,)


###
@widgetlib.provides("ya_ru_button")
def yaRuButton() :
	return ( """
			<a counter="no" type="icon" size="large" name="ya-share"> </a>
			<script charset="utf-8" type="text/javascript">
			if (window.Ya && window.Ya.Share) {
				Ya.Share.update();
			} else {
				(function() {
					if (!window.Ya) {
						window.Ya = {}
					}
					Ya.STATIC_BASE = 'http:\/\/yandex.st\/wow\/2.15.3\/static';
					Ya.START_BASE = 'http:\/\/my.ya.ru\/';
					var shareScript = document.createElement("script");
					shareScript.type = "text/javascript";
					shareScript.async = "true";
					shareScript.charset = "utf-8";
					shareScript.src = Ya.STATIC_BASE + "/js/api/Share.js";
					(document.getElementsByTagName("head")[0] || document.body).appendChild(shareScript);
				})();
			}
			</script>
		""", )

@widgetlib.provides("ya_share_buttons")
@widgetlib.required(js_list=("http://yandex.st/share/share.js",))
def yaShareButtons(services_list) :
	services_list = [
		ulib.validators.common.validRange(item, YA_SHARE_SERVICES_LIST)
		for item in ulib.validators.common.validStringList(services_list)
	]
	return ( """
			<div class="yashare-auto-init" data-yashareL10n="ru" data-yashareType="icon"
			data-yashareQuickServices="%s"></div>
		""" % (",".join(services_list)), )

