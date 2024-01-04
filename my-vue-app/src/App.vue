<template>
  <div>
    <h1>High School Grade Predictor</h1>
    <div class="card">
      <TabMenu :model="items" />
    </div>
    <div v-if="activeTab === 'PredictGrade'">
      <PredictGrade />
    </div>
    <div v-if="activeTab === 'DataViz'">
      <DataViz />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import PredictGrade from './components/PredictGrade.vue';
import DataViz from "@/components/DataViz.vue";
import TabMenu from 'primevue/tabmenu';

const items = ref([
  { label: 'Dashboard', icon: 'pi pi-fw pi-home', command: () => { activeTab.value = 'PredictGrade'; } },
  { label: 'Data Visualization', icon: 'pi pi-fw pi-chart-line', command: () => { activeTab.value = 'DataViz'; } }
]);

const activeTab = ref('PredictGrade');
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.card {
  margin: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
