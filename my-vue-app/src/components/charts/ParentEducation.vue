<template>
  <div class="">
    <Chart type="bar" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chartData = ref(null);
const chartOptions = ref(null);
const parentEducationLabels = [
      "Unknown",

          "some college",


  "associates degree",
          "bachelor's degree",

  "master's degree",

      "high school",

];

onMounted(async () => {
    await fetchParentEducationData();
    chartOptions.value = setChartOptions();
});

const fetchParentEducationData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/parent-education-distribution');
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        chartData.value = setChartData(data);
    } catch (error) {
        console.error('Error:', error);
    }
};

const setChartData = (apiData) => {
    // The order of these labels should match the order of the API response keys
    const dataValues = parentEducationLabels.map((label, index) => apiData[index.toString()] || 0);

    return {
        labels: parentEducationLabels,
        datasets: [
            {
                label: 'Parent Education Level Distribution',
                data: dataValues,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }
        ]
    };
};

const setChartOptions = () => {
    return {
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Parent Education Level'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Students'
                }
            }
        }
    };
};
</script>

<style scoped>
.card {
    padding: 1rem;
}
</style>
