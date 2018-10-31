
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import axios from 'axios'
// axios全局配置
import VueAxios from 'vue-axios'
Vue.use(VueAxios,axios);
Vue.config.productionTip = false

import global_ from './components/Global'//引用文件
Vue.prototype.GLOBAL = global_

new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
