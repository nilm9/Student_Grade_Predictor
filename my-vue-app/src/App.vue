<template>
  <div  class="base">
  <div  class="center">
    <div>

       <Menubar :model="items" class="menu">
            <template #start>
              <img src="../public/logo.png" alt="">
            </template>
      <template #item="{ item, props, hasSubmenu, root }">
                <a v-ripple class="flex align-items-center" v-bind="props.action">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                    <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
                    <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
                    <i v-if="hasSubmenu" :class="['pi pi-angle-down text-primary', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
                </a>
            </template>
            <template #end>
                <div class="search-user">
                    <InputText placeholder="Search Charts" type="text" class="w-8rem sm:w-auto" />
                    <img class="circle-image" src="../public/user.png" alt="" >
                </div>
            </template>
        </Menubar>
    </div>


    <div class="sub-center">


    <div v-if="activeTab === 'Home'">
            <HomeLanding />

    </div>
    <div v-if="activeTab === 'Dashboard'">
      <DashboardCharts />
    </div>
    <div v-if="activeTab === 'PredictGrade'">
      <PredictGrade />
    </div>
    <div v-if="activeTab === 'DataViz'">
      <DataViz />
    </div>
                </div>
  </div>
      </div>

</template>


<script setup>
import { ref } from "vue";
import PredictGrade from './components/PredictGrade.vue';
import DataViz from "@/components/DataViz.vue";
import  Menubar  from 'primevue/menubar';
import  InputText  from 'primevue/inputtext';
import HomeLanding from './components/HomeLanding.vue';
import DashboardCharts from "@/components/DashboardCharts.vue";


const activeTab = ref('Home');

const items = ref([
    {
        label: 'Home',
        icon: 'pi pi-home',
        command: () => { activeTab.value = 'Home'; }
    },
    {
        label: 'Dashboard',
        icon: 'pi pi-chart-bar',
        command: () => { activeTab.value = 'Dashboard'; }
    },
  {
        label: 'PredictGrade',
        icon: 'pi pi-pencil',
        command: () => { activeTab.value = 'PredictGrade'; }
    },
    {
        label: 'Data Visualization',
        icon: 'pi pi-chart-line',
        command: () => { activeTab.value = 'DataViz'; }
    }
]);




</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
}


.card, .container{
  margin: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.25);
}

img {
  width: 7rem;
}



.circle-image {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  object-fit: cover;
}

.search-user {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-right:2rem;
}

.p-menuitem-content span {
  margin: 0rem .3rem 0rem  0rem !important;
}

.base{
  display:flex;
  flex-direction:column;
  justify-content: center;
  align-items: center;
}
.center{

  width:85vw;
}
.sub-center{
  margin:0rem 10%;

}
.p-menubar.p-component.menu{
  padding:0rem !important;
}
</style>
