<template>

  <div class="container">

      <div class="layout-outer">

    <form @submit.prevent="submitForm" class="prediction-form">
      <div class="stacked">
              <div >


      <div class="form-group">
        <label for="NrSiblings">Number of Siblings:</label>
        <InputText id="NrSiblings" v-model="formData.NrSiblings" />
      </div>
      <div class="form-group">
        <label for="ReadingScore">Reading Score:</label>
        <InputText id="ReadingScore" v-model="formData.ReadingScore" />
      </div>
      <div class="form-group">
        <label for="WritingScore">Writing Score:</label>
        <InputText id="WritingScore" v-model="formData.WritingScore" />
      </div>
      <div class="form-group">
        <label for="LinguisticScore">Linguistic Score:</label>
        <InputText id="LinguisticScore" v-model="formData.LinguisticScore" />
      </div>
<div class="form-group">
  <label for="gender">Gender:</label>
  <SelectButton id="gender" v-model="selectedGender" :options="genderOptions" optionLabel="name" />
</div>

                <div class="form-group">
  <label>Ethnic Group:</label>
                  <div class=" centered">
    <div v-for="option in ethnicGroupOptions" :key="option.value" class="form-group centered">

      <RadioButton v-model="selectedEthnicGroup" :inputId="option.value" name="ethnicGroup" :value="option.value" />
      <label :for="option.value">{{ option.name }}</label>
    </div>
                        </div>

  </div>
</div>
              <div class="form-group binary-layout">
        <div class="col-bin">
          <div class="label-input-group">
            <label for="LunchType_standard">Standard Lunch:</label>
            <InputSwitch id="LunchType_standard" v-model="formData.LunchType_standard" />
          </div>

          <div class="label-input-group">
            <label for="TestPrep_completed">Test Preparation Completed:</label>
            <InputSwitch id="TestPrep_completed" v-model="formData.TestPrep_completed" />
          </div>

          <div class="label-input-group">
            <label for="TestPrep_none">No Test Preparation:</label>
            <InputSwitch id="TestPrep_none" v-model="formData.TestPrep_none" />
          </div>

          <div class="label-input-group">
            <label for="ParentMaritalStatus_divorced">Parent Marital Status Divorced:</label>
            <InputSwitch id="ParentMaritalStatus_divorced" v-model="formData['ParentMaritalStatus_divorced']" />
          </div>

          <div class="label-input-group">
            <label for="ParentMaritalStatus_married">Parent Marital Status Married:</label>
            <InputSwitch id="ParentMaritalStatus_married" v-model="formData['ParentMaritalStatus_married']" />
          </div>
        </div>

        <div class="col-bin">
          <div class="label-input-group">
            <label for="ParentMaritalStatus_single">Parent Marital Status Single:</label>
            <InputSwitch id="ParentMaritalStatus_single" v-model="formData['ParentMaritalStatus_single']" />
          </div>

          <div class="label-input-group">
            <label for="ParentMaritalStatus_widowed">Parent Marital Status Widowed:</label>
            <InputSwitch id="ParentMaritalStatus_widowed" v-model="formData['ParentMaritalStatus_widowed']" />
          </div>

          <div class="label-input-group">
            <label for="TransportMeans_private">Private Transport:</label>
            <InputSwitch id="TransportMeans_private" v-model="formData.TransportMeans_private" />
          </div>

          <div class="label-input-group">
            <label for="TransportMeans_school_bus">School Bus Transport:</label>
            <InputSwitch id="TransportMeans_school_bus" v-model="formData.TransportMeans_school_bus" />
          </div>
        </div>
      </div>

      </div>

      <Button type="submit" label="Predict" class="submit-button" @click="startPrediction" />
    </form>

  </div>

  </div>

        <form  class="result-form">
    <div class="">
      <h2>Your Prediction</h2>
      <div class="prediction-container">
        <ProgressBar mode="indeterminate" style="height: 6px; margin-top:2rem;" v-if="isLoading"></ProgressBar>

        <!-- Display prediction result if available -->
        <div class="result" v-if="predictionResult">
          Prediction: {{ predictionResult }}
        </div>

        <!-- Placeholder when there is no prediction and not loading -->
        <div class="placeholder" v-if="!predictionResult && !isLoading">
          <p>Enter your data to get your final grade.</p>
        </div>
      </div>
    </div>
        </form>
</template>

<script setup>
import { ref } from 'vue';
import { watch } from 'vue';

import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import Button from 'primevue/button';
import SelectButton from 'primevue/selectbutton';
import RadioButton from 'primevue/radiobutton';
import ProgressBar from 'primevue/progressbar';

const predictionResult = ref(null);
//const progressValue = ref(0);
//const showProgressBar = ref(false);

const isLoading = ref(false);


const genderOptions = [
  { name: 'Male', value: 'male' },
  { name: 'Female', value: 'female' }
];

const ethnicGroupOptions = [
  { name: 'A', value: 'A' },
  { name: 'B', value: 'B' },
  { name: 'C', value: 'C' },
  { name: 'D', value: 'D' },
  { name: 'E', value: 'E' }
];


const formData = ref({
  NrSiblings: '',
  ReadingScore: '',
  WritingScore: '',
  LinguisticScore: '',
  Gender_male: false,
  'EthnicGroup_group A': false,
  'EthnicGroup_group B': false,
  'EthnicGroup_group C': false,
  'EthnicGroup_group D': false,
  'EthnicGroup_group E': false,
  LunchType_standard: false,
  TestPrep_completed: false,
  TestPrep_none: false,
  'ParentMaritalStatus_divorced': false,
  'ParentMaritalStatus_married': false,
  'ParentMaritalStatus_single': false,
  'ParentMaritalStatus_widowed': false,
  TransportMeans_private: false,
  TransportMeans_school_bus: false,
});

const selectedGender = ref(formData.value.Gender_male ? 'male' : 'female');
const selectedEthnicGroup = ref('');

watch(selectedGender, (newGender) => {
  formData.value.Gender_male = newGender === 'male';
});

watch(selectedEthnicGroup, (newValue) => {
  // Reset all ethnic group values to false
  formData.value['EthnicGroup_group A'] = false;
  formData.value['EthnicGroup_group B'] = false;
  formData.value['EthnicGroup_group C'] = false;
  formData.value['EthnicGroup_group D'] = false;
  formData.value['EthnicGroup_group E'] = false;

  // Set the selected ethnic group to true
  if (newValue) {
    formData.value[`EthnicGroup_group ${newValue}`] = true;
  }
});

watch(formData, (newValue) => {
  console.log('Form Data changed:', newValue);
}, { deep: true }); // 'deep: true' is important to watch nested properties



console.log(formData)


const submitForm = async () => {
  console.log('clicking')
  try {
    const response = await fetch('http://127.0.0.1:5000/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData.value),
    });
    const data = await response.json();
    predictionResult.value = data.prediction;
  } catch (error) {
    console.error('Error:', error);
  }
};

const startPrediction = async () => {
  isLoading.value = true;

  // Delay the API call for 2 seconds
  setTimeout(async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData.value),
      });
      const data = await response.json();
      predictionResult.value = data.prediction;
    } catch (error) {
      console.error('Error:', error);
    } finally {
      isLoading.value = false; // Hide progress bar after the prediction is fetched
    }
  }, 3000); // 2000 milliseconds = 2 seconds
};

</script>

<style>
.container {

  max-width: 1000px;
  margin: 0 auto;
  padding: 3rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
  width:70rem;
}

h1 {
  text-align: center;
  color: #333;
}
.prediction-form{
width: 100%;
}
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #444;
}

.submit-button {
  padding: 1rem 4rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: .75rem;
  cursor: pointer;
}

.centered{
  display:flex;
  flex-direction:row;
  align-items: center;
  justify-content: center;
  margin: 0rem .2rem;

}

.sm{
    margin: 0rem .2rem;

}
.submit-button:hover {
  background-color: #0056b3;
}
.binary-layout{
    display: flex;
  flex-direction: row;
}
.col-bin{


    display: flex;
  flex-wrap: wrap;
}
.stacked{
   display: flex;
  flex-direction: row;
}
.result {
  margin-top: 20px;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  text-align: center;
}
.label-input-group{
  display:flex;
  flex-direction: row;
  justify-content: space-between;
  text-align:left;
  gap:3rem;
  padding:0rem 3rem;
}
.label-input-group label  {
  width:10rem;
}
.result-form{
  margin:3rem;
}
.prediction-container{
    max-width: 1000px;
  margin: 2rem auto;
  padding: 3rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
}

</style>