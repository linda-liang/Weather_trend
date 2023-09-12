<template>
<div>
  <div id="chartTop10Food" style="width:100%; height:640px;margin-top: 20px;margin-left: 20px;"></div>
</div>
</template>

<script>
import {
  Message
} from 'element-ui'
export default {
  data() {
    return {
      chartTop10Food: null,
      chart_option: {
        title: {
          text: '上海最火的10道菜'
        },
        grid: {
          left: "15",
          containLabel: true,
        },
        tooltip: {},
        // legend: {
        //   // data: ['频次']
        // },
        xAxis: [
          //x轴数据设置
          {
            type: "value",
            // name: "频次",
            min: 0,
            axisLabel: {
              formatter: "{value} ",
            },
            splitLine: {
              show: false,
            },
            axisLine: {
              lineStyle: {
                color: "#65C6E7",
              },
            },
          },
        ],
        yAxis: {
            // type: "category",
            axisLine: {
              //这是x轴文字颜色
              show:false,
              lineStyle: {
                color: "#65C6E7",
              },
            },
            axisTick:{
              show:false,
              alignWithLabel:true,
              interval: 1
            },
            axisLabel:{
              interval:0,
              // rotate:45
            },
            data: []
          },
        series: [
          {
            name: '频次',
            type: 'bar',
            data: [],
            barGap: '50%',
            barWidth: '40%',
            label: {
              show: true,
            },
            itemStyle: {
              //通常情况下：
                normal: {
                  //每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
                  color: function (params) {
                    var colorList = [
                      "#245B22",
                      "#425BD7",
                      "#855BD7",
                      "#4B6FB8",
                      "#0F6E43",
                      "#B69C2B",
                      "#2588BB",
                      "#BB612D",
                      "#1D9394",
                      "#C24545",
                    ];
                    return colorList[params.dataIndex];
                  },
                },
            }
          }
          
        ]
      },
    };
  },
  created(){
  },
  mounted: function() {
    this.initChart();
    this.getTop10FoodData();
  },
  methods: {
    initChart() {
      this.chartTop10Food = this.$echarts.init(document.getElementById('chartTop10Food'));
      this.chartTop10Food.setOption(this.chart_option);
    },
    getTop10FoodData(){
      let that = this;
        this.req({
          url: "get_top10_food",
          data: {},
          method: "POST"
          }).then(
            res => {
              if(res.success){
                console.log(res);
                that.chart_option.yAxis.data=res.content.x;
                that.chart_option.series[0].data=res.content.y;
                that.chartTop10Food.setOption(that.chart_option);
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