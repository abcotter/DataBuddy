<template>
	<div class="home">
		<h1>DATA BUDDY</h1>

		<h3>
			Upload an image file for of data, and get it it in a csv form below to
			skip manual data entry!
		</h3>
		<h5>
			Please note: this uses pytesseract to perform the OCR component. The
			program is not 100% accurate, so ensure you validate your data after
			converting to a usable form.
		</h5>
		<form action="/action_page.php">
			<input
				type="file"
				id="myfile"
				name="myfile"
				@change="onFileChange"
			/><br /><br />
		</form>
		<div v-if="convertedData" class="data" id="data">
			<span v-for="data in convertedData" :key="data" contenteditable>
				{{ data }} <br />
			</span>
		</div>
		<button v-if="convertedData" class="copy" @click="copyData">COPY</button>
	</div>
</template>

<script>
import axios from "axios";

export default {
	name: "HelloWorld",
	data() {
		return {
			image: null,
			convertedData: null,
		};
	},
	methods: {
		onFileChange(e) {
			var files = e.target.files || e.dataTransfer.files;
			if (!files.length) return;
			this.createImage(files[0]);
		},
		copyData() {
			var copyText = document.getElementById("data").innerText;
			var input_temp = document.createElement("textarea");
			input_temp.innerHTML = copyText;
			input_temp.select();
			input_temp.setSelectionRange(0, 99999); /*For mobile devices*/
			document.execCommand("copy");
			alert(input_temp.value);
		},
		createImage(file) {
			var reader = new FileReader();
			var vm = this;

			reader.onload = (e) => {
				vm.image = e.target.result;
			};
			reader.readAsDataURL(file);
		},
	},
	watch: {
		image() {
			var formData = new FormData();

			let image = this.image.split("base64,")[1];

			formData.append("file", image);

			const baseURI = "http://127.0.0.1:5000/getCSV";
			axios
				.post(baseURI, formData, {
					headers: {
						"Content-Type": "multipart/form-data",
					},
				})
				.then((result) => {
					this.convertedData = result.data.result;
				})
				.catch((error) => {
					console.log(error);
				});
		},
	},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.data {
	width: 800px;
	height: 400px;
	background-color: rgb(232, 234, 235);
	margin: auto;
	padding-top: 20px;
	overflow: scroll;
	position: relative;
}

.data::-webkit-scrollbar {
	-webkit-appearance: none;
}

.data::-webkit-scrollbar:vertical {
	width: 11px;
}

.data::-webkit-scrollbar:horizontal {
	height: 0px;
}

.data::-webkit-scrollbar-thumb {
	border-radius: 8px;
	border: 2px solid rgb(232, 234, 235); /* should match background, can't be transparent */
	background-color: rgba(0, 0, 0, 0.5);
}

.copy {
}
</style>
