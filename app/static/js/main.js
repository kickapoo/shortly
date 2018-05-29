
var app = new Vue({
	el: '#app',
	data: {
		placeholder:'Paste a link to shorten it',
		raw_lng_url:'',
		srt_url:'',
		lng2str_url:'',
		form_errors:[],
	},
	methods: {
		copyShortUrl2Clipboard() {
			copyText = document.getElementById("srt_url_result")
			copyText.select();
			document.execCommand('copy');
		},
		onSubmit: function(){
			const vm = this;
			vm.form_errors = [];
			vm.srt_url = '';
			vm.lng2str_url = vm.raw_lng_url
			// request config
			var shortmeOptions = {
				headers: {
					'Content-Type': 'Application/Json',
				},
				data: {
					raw_lng_url: vm.raw_lng_url
				}
			}
			axios.post('/api/short-me', shortmeOptions)
			.then(response => {
				vm.srt_url = response.data.data.srt_url;
			})
			.catch(function (error) {
				if (error.response){
					error.response.data.errors.forEach(function(er) {
						vm.form_errors.push(er)
					});
				}
			 });
			this.raw_lng_url = ''
		}
	}
})
