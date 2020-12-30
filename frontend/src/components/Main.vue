<template>
	<div class="home">
		<h1>DATA BUDDY</h1>

		<h3>
			Upload an image file for of data, and get it it in a csv form below to
			skip manual data entry!
		</h3>
		<form action="/action_page.php">
			<input
				type="file"
				id="myfile"
				name="myfile"
				@change="onFileChange"
			/><br /><br />
		</form>
		<div v-if="convertedData">
			<span v-for="data in convertedData" :key="data">{{ data }} <br /></span>
		</div>
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
					console.log(result);
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
</style>
