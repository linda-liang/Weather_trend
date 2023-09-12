<template>
<div>
  <div id="chartMap" style="width:100%; height:400px;margin-top:20px;"></div>
  <div id="chartDistPie" style="width:100%; height:400px;"></div>
  <div id="chartShopBar" style="width:100%; height:400px;"></div>
  <div id="chartStarRatio" style="width:100%; height:400px;"></div>
  <div id="chartFoodType" style="width:100%; height:400px;"></div>
  <div id="chartPriceScore" style="width:100%; height:400px;"></div>
  <div id="chartCloud" style="width:100%; height:500px;;margin-bottom:40px;"></div>
</div>
</template>

<script>
import {
  Message
} from 'element-ui'
import echarts from 'echarts'
import shanghai from "@/assets/shanghai.json"
export default {
  data() {
    return {
      chartDistPie: null,
      chartShopBar: null,
      chartStarRatio: null,
      chartFoodType: null,
      chartPriceScore: null,
      chartCloud: null,
      chartMap:null,
      cloudData:[],
      pie_option: {
        title: {
          text: '行政区美食分布'
        },
          series: [
            {
              type: 'pie',
              data: []
            }
          ]
      },
      bar_option: {
        title: {
          text: '商圈美食分布'
        },
        tooltip: {},
        legend: {
          data: ['数量']
        },
        xAxis: {
          data: [],
          // type: 'category'
          axisTick:{
            alignWithLabel:true,
            interval: 1
          },
          axisLabel:{
            interval:0,
            rotate:45
          }
        },
        yAxis: {},
        series: [
          {
            name: '数量',
            type: 'bar',
            data: [],
            barGap: '50%',
            barWidth: '60%'
          }
        ]
      },
      star_ratio_option: {
        title: {
          text: '星级分布'
        },
          series: [
            {
              type: 'pie',
              data: []
            }
          ]
      },
      food_type_bar_option: {
        title: {
          text: '美食种类分布'
        },
        tooltip: {},
        legend: {
          data: ['美食种类数量']
        },
        xAxis: {
          data: [],
          // type: 'category'
          axisTick:{
            alignWithLabel:true,
            interval: 1
          },
          axisLabel:{
            interval:0,
            rotate:45
          }
        },
        yAxis: {},
        series: [
          {
            name: '美食种类数量',
            type: 'bar',
            data: [],
            barGap: '50%',
            barWidth: '60%'
          }
        ]
      },
      price_score_option: {        
        title: {
            text: '人均消费与综合评分散点'
          },
        xAxis: {
          name: "人均价格",
          data: []
        },
        yAxis: {name: "评分"},
        series: [
          {
            type: 'scatter',
            data: [],
            symbolSize:6,
            itemStyle:{
              color:'#00c0c0'
            }
          }
        ]
      },
      cloud_option:{
      },
      map_option:{
        title: {
          text: '上海美食地域分布'
        },
        //鼠标放上去的文字提示
        tooltip: {
          padding: 0,
          backgroundColor: '#6B99FF',
          padding: 10, 
          textStyle:{
            color:'#fff',
            lineHeight:'18px'
          },
          formatter: params => {
            return params.name + '<br/>' + "共计：" + params.value + "家";
          }
        },
        visualMap: {
          min: 0,
          max: 500,
          top:'7%',
          right:"84%",
          show: true,
          splitNumber: 5,
          inRange: {
            color: ['#cceecc','#cceecc','#cceecc','#cceecc','#eeee00','#ff0000']
          },
          textStyle: {
            color: '#444'
          },
          splitList: [   
            {start: 10000, end:50000},{start: 7000, end: 10000},  
            {start: 5000, end: 7000},{start: 3000, end: 5000},  
            {start: 1000, end: 3000},{start: 0, end: 1000},  
          ],  
        },
        geo: {
          map: 'shanghai',
          show:true,
          label: {
              show: true,
              color: '#fff'
          },
          roam: false,
          itemStyle: {
              areaColor: '#feb6aa',
              borderColor: '#fff',
              borderWidth: 1,
          },
          left: '5%',
          right: '5%',
          top: '5%',
          bottom: '5%'
        },
        series: [{
          name: '',
          type: 'map',
          mapType: 'shanghai', 
          geoIndex: 0, // 不可缺少，否则无tooltip 指示效果
          data: [],
        }],
      }
    };
  },
  created(){
  },
  mounted: function() {
    this.initChart();
    this.getDistrictPieData();    
    this.getShopBarData();    
    this.getStartRatioData();    
    this.getFoodTypeBarData();
    this.getPriceScoreData();
    this.getCloudData();
    this.getMapData();
  },
  methods: {
    handleAvatarSuccess(res, file){
      this.imageUrl = URL.createObjectURL(file.raw);
      console.log(res.content);
      this.classifyBigType = res.content.label_big;
      this.classifySmallType = res.content.label_small;
      this.modelName = res.content.model_name;
      // this.heatMapSrc = "data:image/jpg;base64,"+res.content.heatmap;
    },
    getDistrictPieData(){
      let that = this;
        this.req({
          url: "district_pie",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                // console.log(res);
                that.pie_option.series[0].data=res.content;
                that.chartDistPie.setOption(that.pie_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    getMapData(){
      let that = this;
        this.req({
          url: "map_data",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                console.log(res);
                that.map_option.series[0].data=res.content;
                that.chartMap.setOption(that.map_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    getShopBarData(){
      let that = this;
        this.req({
          url: "shopping_num_bar",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                // console.log(res);
                that.bar_option.xAxis.data=res.content.x;
                that.bar_option.series[0].data=res.content.y;
                that.bar_option.xAxis.splitNumber = res.content.x.length;
                that.chartShopBar.setOption(that.bar_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    getStartRatioData(){
      let that = this;
        this.req({
          url: "star_ratio_pie",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                // console.log(res);
                that.star_ratio_option.series[0].data=res.content;
                that.chartStarRatio.setOption(that.star_ratio_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    getFoodTypeBarData(){
      let that = this;
        this.req({
          url: "food_type_bar",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                // console.log(res);
                that.food_type_bar_option.xAxis.data=res.content.x;
                that.food_type_bar_option.series[0].data=res.content.y;
                that.food_type_bar_option.xAxis.splitNumber = res.content.x.length;
                that.chartFoodType.setOption(that.food_type_bar_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    getPriceScoreData(){
      let that = this;
        this.req({
          url: "price_score_scatter",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                // console.log(res);
                that.price_score_option.xAxis.data=res.content.x;
                that.price_score_option.series[0].data=res.content.y;
                that.chartPriceScore.setOption(that.price_score_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    getCloudData(){
      let that = this;
        this.req({
          url: "word_cloud",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                console.log(res);
                that.cloudData=res.content;
                that.cloud_option={
                  title: {
                    text: '美食词云图'
                  },
                  grid:{
                    top:100,
                    left:100,
                    containLabel: true,
                  },
                  xAxis:{
                    show:false
                  },
                  yAxis:{
                    show:false
                  },
                  series: [{
                    type: 'custom',
                    data: that.cloudData,
                    renderItem(params, api){
                      return {
                        type:'text',
                        x:(Math.random()+0.25) * 500,
                        y: (Math.random()+0.1) * 500,
                        style:{
                          text: that.cloudData[params.dataIndex].name,
                          fontSize:that.cloudData[params.dataIndex].value,
                          fill: `rgba(${Math.floor(Math.random() * 257)},${Math.floor(Math.random() * 257)},${Math.floor(Math.random() * 257)}, ${Math.random()})`
                        }
                      }
                    }
                  }]
                }
                that.chartCloud.setOption(that.cloud_option);
            }},
            err => {
              Message({
                  message: '获取模型列表失败',
                  type: 'warning',
                  duration: 3 * 1000
                })
            }
        );
    },
    initChart() {
      this.$echarts.registerMap('shanghai', shanghai);
      this.chartMap = this.$echarts.init(document.getElementById('chartMap'));
      this.chartMap.setOption(this.map_option);
      this.chartDistPie = this.$echarts.init(document.getElementById('chartDistPie'));
      this.chartDistPie.setOption(this.pie_option);
      this.chartShopBar = this.$echarts.init(document.getElementById('chartShopBar'));
      this.chartShopBar.setOption(this.bar_option);
      this.chartStarRatio = this.$echarts.init(document.getElementById('chartStarRatio'));
      this.chartStarRatio.setOption(this.star_ratio_option);
      this.chartFoodType = this.$echarts.init(document.getElementById('chartFoodType'));
      this.chartFoodType.setOption(this.food_type_bar_option);
      this.chartPriceScore = this.$echarts.init(document.getElementById('chartPriceScore'));
      this.chartPriceScore.setOption(this.price_score_option);
      this.chartCloud = this.$echarts.init(document.getElementById('chartCloud'));
      this.chartCloud.setOption(this.cloud_option);
    }
  }
};
</script>

<style lang="scss">
.top-row {
  width: 100%;
  height: 40px;
  margin-top:20px;
  margin-left:20px;
  .add-button{
    display: inline-block;
    margin-right: 10px;
  }
  .left_div{
    display: inline-block;
  }
  .right_div{
    display: inline-block;
  }
}
.appoinment_win{
  .line{
    margin-left:10px;
    margin-top:20px;
    .label{
      display: inline-block;
      width:100px;
    }
    .content{
      display: inline-block;
    }
  }
}
.el-upload{
  margin: 0;
  padding: 0;
  width:100%;
}
.el-upload--text{
  margin: 0;
  padding: 0;
  width:100%;
}
</style>