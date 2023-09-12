import Vue from 'vue'
import * as echarts from 'echarts'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'
import request from '@/utils/request'

import '@/icons' // icon
// import '@/permission' // permission control
// import BaiduMap from 'vue-baidu-map'

Vue.prototype.$echarts = echarts
// set ElementUI lang to EN
Vue.use(ElementUI, { locale })
// Vue.use(BaiduMap, {
//   ak: 'B1RlLrTGOLsCjYf8lQfvPDel5E70c2gO'    //这个地方是官方提供的ak密钥
// })

Vue.prototype.req = request

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
