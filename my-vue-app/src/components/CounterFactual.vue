<template>
  <div class="counterfactual-analysis">
    <h2>Counterfactual Analysis</h2>
    <div class="form-group">
      <label for="desiredMark">Desired Mark:</label>
      <InputText id="desiredMark" v-model="desiredMark" />
    </div>
    <Button label="Analyze" @click="performAnalysis" />

   <div v-if="analysisResult">
    <h3>Required Changes</h3>
    <ul>

      <li v-if="analysisResult.increaseInStudyHours !== undefined">
        Increase in Weekly Study Hours: {{ analysisResult.increaseInStudyHours }}
      </li>
    </ul>
  </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';


const props = defineProps({
  currentFeatures: Object
});


// Initialize originalWklyStudyHours with the original value of weekly study hours
const originalWklyStudyHours = ref(0);

const desiredMark = ref('');
const analysisResult = ref(null);

const performAnalysis = async () => {
  try {
    console.log("enters")
    const response = await fetch('http://127.0.0.1:5000/api/counterfactual-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
       // body: JSON.stringify({ current_features: formData.value }),
              body: JSON.stringify({
        current_features: props.currentFeatures, // Use the passed props here
        desired_prediction: parseInt(desiredMark.value, 10)
      })
    });
    if (response.ok) {
      const data = await response.json();
              console.log("hello")

      console.log(data)
      // Assuming 'WklyStudyHours' is at the 4th index
      const newWklyStudyHours = data.counterfactual[4];
      const increaseInHours = newWklyStudyHours - originalWklyStudyHours.value;

      analysisResult.value = { ...data, increaseInStudyHours: increaseInHours };
    }
  } catch (error) {
        console.log("fails")

    console.error('Error:', error);
  }
};
</script>

<style scoped>
.counterfactual-analysis {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
}
</style>
