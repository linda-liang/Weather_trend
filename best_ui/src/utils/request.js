import axios from 'axios'
import {
  Message
} from 'element-ui'
// create an axios instance
const service = axios.create({
  baseURL: "/api", // url = base url + request url
  // baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 50000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // config.headers['Content-Type'] = 'application/x-www-form-urlencoded',
    // do something before request is sent
    config.headers.Authorization = 'Bearer '+localStorage.getItem('token')
    // if(config.method === 'post') {
    //   config.data = qs.stringify( {
    //       ...config.data
    //   })
    // } 
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  
  
  response => {
    const res = response.data

    // if the custom code is not 100, it is judged as an error.
    if (!res.success) {
      Message({
        message: res.content.errorMessage || 'Error check your token or method',
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(new Error(res.msg || 'Error'))
    } else {
      return res
    }
  },
  error => {
    console.log('err：' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 2 * 1000
    })
    console.log("login out");
    localStorage.removeItem('classifyHasLogin')
    localStorage.removeItem('is_admin')
    localStorage.removeItem('userId')
    localStorage.removeItem('token')
    this.$router.push({ path: "/login" })
    return Promise.reject(error)
  }
)

export default service.request
