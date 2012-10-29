# -*- coding: utf-8 -*-


from slib import widgetlib


##### Public methods #####
@widgetlib.provides("google_plus_button")
def googlePlusButton() :
	return ( """
			<div class="g-plusone" data-size="medium" data-annotation="none"></div>
			<script type="text/javascript">
				(function() {
					var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
					po.src = 'https://apis.google.com/js/plusone.js';
					var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
				})();
			</script>
		""", )

