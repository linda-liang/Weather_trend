<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
// 初始element-ui版本-
// "element-ui": "2.7.2",
export default {
  name: 'App'
  // mounted() { 
  //   window.addEventListener('unload', this.unloadHandler)
  // },
  // destory(){
  //   window.removeEventListener('unload', this.unloadHandler)
  // },
  // methods: {
  //   unloadHandler() {
  //     localStorage.removeItem('classifyHasLogin')
  //     localStorage.removeItem('isAdmin')
  //     localStorage.removeItem('userId')
  //     localStorage.removeItem('username')
  //     localStorage.removeItem('token')
  //   }
  // }
}
</script>
<style lang="scss">
.root{
  margin: 50px 25px 0px 25px
}
.my-flex{
  display: flex;
}
</style>
