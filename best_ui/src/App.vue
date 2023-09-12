<template>
  <div id="app">
    <el-row>
      <el-col :span="6"><div class="bg-blue">Best Weather</div></el-col>
      <el-col :span="5">
        <div :class="chart_type=='trend'?'bg-active':'bg-blue'" id="trend" @click="clickTab($event)">
          Trend
        </div>
      </el-col>
      <el-col :span="4">
        <div :class="chart_type=='compare'?'bg-active':'bg-blue'"  id="compare" @click="clickTab($event)">
          Compare
        </div>
      </el-col>
      <el-col :span="5">
        <div :class="chart_type=='ranking'?'bg-active':'bg-blue'"  id="ranking" @click="clickTab($event)">
          Ranking
        </div>
      </el-col>
      <el-col :span="4">
        <div :class="chart_type=='analyze'?'bg-active':'bg-blue'"  id="analyze" @click="clickTab($event)">
          Analyze
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6" class="left-bar">
        <div class="line" v-if="chart_type=='trend'">
          <div class="label">Country:</div>
          <div class="in_content">
            <el-select placeholder="Select Country"  v-model="selected_country" @change="selected_city=''">
              <el-option
                v-for="item in countryOp"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line" v-if="chart_type=='trend'||chart_type=='compare'">
          <div class="label">City:</div>
          <div class="in_content">
            <el-select placeholder="Select City"  v-model="selected_city" >
              <el-option
                v-for="item in cities"
                v-show="chart_type!='trend'||item.country==selected_country"
                :key="item.city"
                :label="item.city"
                :value="item.city">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line" v-if="chart_type=='compare'">
          <div class="label">City2:</div>
          <div class="in_content">
            <el-select placeholder="Select City2"  v-model="selected_city2">
              <el-option
                v-for="item in cities"
                :key="item.city"
                :label="item.city"
                :value="item.city">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line">
          <div class="label">Attr:</div>
          <div class="in_content">
            <el-select placeholder="Select Attr"  v-model="selected_attr">
              <el-option
                v-for="item in (chart_type=='analyze'?anaAttr:attrs)"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line" v-if="chart_type=='analyze'">
          <div class="label">Attr2:</div>
          <div class="in_content">
            <el-select placeholder="Select Attr2"  v-model="selected_attr2">
              <el-option
                v-for="item in anaAttr"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line">
          <div class="label">Start:</div>
          <div class="in_content">
            <el-date-picker
              v-model="start_date"
              type="date"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              default-value="2012-10-01"
              placeholder="Select Start Date">
            </el-date-picker>
          </div>      
        </div>
        <div class="line">
          <div class="label">To:</div>
          <div class="in_content">
            <el-date-picker
              v-model="end_date"
              type="date"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              default-value="2017-11-30"
              placeholder="Select End Date">
            </el-date-picker>
          </div>      
        </div>
        <div class="line" v-if="chart_type=='trend'||chart_type=='compare'">
          <div class="label">Period:</div>
          <div class="in_content">
            <el-select placeholder="Select Period"  v-model="period">
              <el-option
                v-for="item in periodOp"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line" v-if="chart_type=='compare'||chart_type=='analyze'">
          <div class="label">Chart</div>
          <div class="in_content">
            <el-select placeholder="Select Chart Type"  v-model="c_type">
              <el-option
                v-for="item in chartTypeOp"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </div>      
        </div>
        <div class="line" v-if="chart_type=='ranking'">
          <div class="label">Order</div>
          <div class="in_content">
            <el-switch
              v-model="ranking_order"
              active-color="#13ce66"
               inactive-color="#ff4949"
              active-text="descending"
              inactive-text="ascending">
            </el-switch>
          </div>      
        </div>
        <div class="line">
          <el-button type="primary" @click="generate">Generate</el-button>
        </div>
        <div class="line" v-if="(chart_type=='trend'||chart_type=='compare')&&(selected_city!=''||selected_city2!='')">
          <div style="color:#ffffff" v-if="selected_city!=''">
            {{ selected_city }}:&nbsp&nbsp(<span v-for="item in cities" :key="item.city" v-show="item.city==selected_city">{{ item.longitude }},{{ item.latitude }}</span>)
          </div>
          <div style="color:#ffffff" v-if="selected_city2!=''&&chart_type=='compare'">
            {{ selected_city2 }}:&nbsp&nbsp(<span v-for="item in cities" :key="item.city" v-show="item.city==selected_city2">{{ item.longitude }},{{ item.latitude }}</span>)
          </div>
        </div>
        <div class="line" style="text-align: left;padding-left: 10px;">
          <div class="label">Count:</div>
          <div class="label">{{ total_count }}</div>  
          <el-button type="primary" style="margin-left: 20px;" @click="get_total_count">Get</el-button>
        </div>
      </el-col>
      <el-col :span="18" class="content-body">
        <div id="chart" class="chart-div"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
    // VeLine
  },
  data() {
    return {
      chart_type: 'trend',
      chart:null,
      total_count:0,
      cities:[],
      attrs:[],
      selected_country:'',
      selected_city:'',
      selected_city2:'',
      c_type:'',
      selected_attr:'',
      selected_attr2:'',
      start_date:'',
      end_date:'',
      period:'',
      tooltip_city:[],
      analyze_y:[],
      ranking_order:true,
      countryOp:[

      ],
      periodOp:[
        'day', 'week', 'month'
      ],
      chartTypeOp:['line','bar','scatter'],
      anaAttr: ['humidity', 'pressure', 'temperature', 'weather_description', 'wind_direction', 'wind_speed', 'latitude', 'longitude'],
      line_chart_option: {
        title: {
          text: 'Trend'
        },
        backgroundColor:'#ffffff',
        tooltip: {},
        legend: {
          // data: ['数量']
        },
        xAxis: {
          data: [1,2,3,4,5],
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
            name: '',
            type: 'line',
            data: [2,4,6,4,7],
            // barGap: '50%',
            // barWidth: '60%'
          }
        ]
      }
    };
  },
  created(){
    this.get_city_info();
    this.get_attrs_info();
  },
  mounted: function() {
    this.chart = this.$echarts.init(document.getElementById('chart'));
    this.chart.setOption(this.line_chart_option);
  },
  methods:{
    clickTab(event) {
      if(event.currentTarget.id!=this.chart_type){
        this.chart_type=event.currentTarget.id;
      }
    },
    get_total_count(){
      let that = this;
      this.req({
        url: "get_data_count",
        data: {},
        method: "POST"
        }).then(
          res => {
            if(res.success){
              that.total_count=res.content;
          }},
          err => {
            Message({
                message: '获取数据总量失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    get_city_info(){
      let that = this;
      this.req({
        url: "city_info",
        data: {},
        method: "POST"
        }).then(
          res => {
            if(res.success){
              that.cities=res.content;
              that.countryOp=res.country_list;
          }},
          err => {
            Message({
                message: '获取城市列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    get_attrs_info(){
      let that = this;
      this.req({
        url: "attr_info",
        data: {},
        method: "POST"
        }).then(
          res => {
            if(res.success){
              that.attrs=res.content;
          }},
          err => {
            Message({
                message: '获取城市列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    get_city_attr_line(){
      let that = this;
      this.req({
        url: "city_attr_line",
        data: {
          city:that.selected_city,
          attr:that.selected_attr,
          st:that.start_date,
          et:that.end_date,
          period:that.period
        },
        method: "POST"
        }).then(
          res => {
            if(res.success){
              that.line_chart_option.xAxis.data=res.content.x;
              that.line_chart_option.series[0].data=res.content.y;
              that.chart.setOption(that.line_chart_option);
          }},
          err => {
            Message({
                message: '获取城市列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    get_city_compare(){
      let that = this;
      this.req({
        url: "compare_city",
        data: {
          city:that.selected_city,
          city2:that.selected_city2,
          attr:that.selected_attr,
          st:that.start_date,
          et:that.end_date,
          period:that.period
        },
        method: "POST"
        }).then(
          res => {
            if(res.success){
              let chart_option= {
                title: {
                  text: that.selected_city+' vs. ' +that.selected_city2
                },
                backgroundColor:'#ffffff',
                tooltip: {},
                legend: {
                  data: [that.selected_city, that.selected_city2]
                },
                xAxis: {
                  data: res.content.x,
                  axisLabel:{
                    rotate:45
                  }
                },
                yAxis: {},
                series: [
                  {
                    name: that.selected_city,
                    type: that.c_type==''?'line':that.c_type,
                    data: res.content.y1
                  },
                  {
                    name: that.selected_city2,
                    type: that.c_type==''?'line':that.c_type,
                    data: res.content.y2
                  }
                ]
              }
              that.chart.setOption(chart_option);
          }},
          err => {
            Message({
                message: '获取城市列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    get_ranking(){
      let that = this;
      this.req({
        url: "ranking",
        data: {
          attr:that.selected_attr,
          st:that.start_date,
          et:that.end_date,
          descending:that.ranking_order
        },
        method: "POST"
        }).then(
          res => {
            if(res.success){
              let chart_option= {
                title: {
                  text: that.selected_attr+' ranking'
                },
                backgroundColor:'#ffffff',
                tooltip: {},
                legend: {
                  data: [that.selected_attr]
                },
                grid: {
                  left: "5",
                  containLabel: true,
                },
                xAxis: [
                  {
                    type: "value",
                    // min: 0,
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
                  }
                ],
                yAxis: {
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
                  data: res.content.x
                },
                series: [
                  {
                    name: that.selected_city,
                    type: 'bar',
                    data: res.content.y,
                    // barGap: '50%',
                    // barWidth: '30%',
                    // label: {
                      // show: true,
                    // }
                  }
                ]
              }
              that.chart.clear();
              that.chart.setOption(chart_option);
          }},
          err => {
            Message({
                message: '获取城市列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    get_analyze(){
      let that = this;
      this.req({
        url: "analyze",
        data: {
          // city:that.selected_city,
          attr:that.selected_attr,
          attr2:that.selected_attr2,
          // period:that.period,
          st:that.start_date,
          et:that.end_date
        },
        method: "POST"
        }).then(
          res => {
            if(res.success){
              that.tooltip_city = res.content.name;
              that.analyze_y = res.content.y;
              let chart_option= {
                title: {
                  text: that.selected_attr+' and '+that.selected_attr2
                },
                backgroundColor:'#ffffff',
                tooltip: {
                  formatter: (params) => {
                    let index = params.dataIndex 
                    let obj = that.tooltip_city[index] // 通过索引取当前项完整的接口返回值
                    let str = obj + "," +that.analyze_y[index]
                    return str
                  }
                },
                legend: {
                  data: [that.selected_attr, that.selected_attr2]
                },
                grid: {
                  left: "5",
                  containLabel: true,
                },
                xAxis: {
                  data: res.content.x,
                  name:that.selected_attr,
                  axisLabel:{
                    rotate:45
                  }
                },
                yAxis:{
                  name:that.selected_attr2,
                },
                // yAxis: [{
                //     type: 'value',
                //     name:that.selected_attr,
                //     min: res.content.min_max[0],
                //     max: res.content.min_max[1],
                //     splitLine: {
                //       //去除网格线
                //       show: false,
                //     },
                //     axisLabel: {
                //       // 设置y轴的文字的样式
                //       textStyle: {
                //         show: true,
                //         color: "#BDBDBD",
                //         fontSize: "12",
                //       },
                //     },
                //     // interval: 1,
                //     // splitNumber: 6, //设置坐标轴的分割段数
                //   },
                //   {
                //     type: 'value',
                //     name:that.selected_attr2,
                //     min: res.content.min_max[2],
                //     max: res.content.min_max[3],
                //     splitLine: {
                //       //去除网格线
                //       show: false,
                //     },
                //     axisLabel: {
                //       // 设置y轴的文字的样式
                //       textStyle: {
                //         show: true,
                //         color: "#BDBDBD",
                //         fontSize: "12",
                //       },
                //     },
                //     // interval: 25,
                //     // splitNumber: 6, //设置坐标轴的分割段数
                //   }
                // ],
                series: [
                  {
                    name: that.selected_attr2,
                    type: that.c_type==''?'line':that.c_type,
                    data: res.content.y,
                    yAxisIndex: 0,
                  }
                ]
              }
              that.chart.clear();
              that.chart.setOption(chart_option);
          }},
          err => {
            Message({
                message: '获取城市列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
          }
      );
    },
    generate(){
      if(this.chart_type=='trend'){
        this.get_city_attr_line();
      }else if(this.chart_type=='compare'){
        this.get_city_compare();
      }else if(this.chart_type=='ranking'){
        this.get_ranking();
      }else{
        this.get_analyze();
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.el-row {
  &:last-child {
    margin-bottom: 0;
  }
}
.bg-blue {
  background: #1F4E79;
  height:10vh;
  color:#ffffff;
  line-height:10vh;
}
.bg-active {
  background: #2E75B6;
  height:10vh;
  color:#ffffff;
  line-height:10vh;
}
.left-bar{
  // line-height: 89vh;
  height:89vh;
  background-color: #2E75B6;
  .line {
    margin-top: 30px;
    margin-bottom: 10px;
    max-width:90%;
    .label{
      display:inline-block;
      width:18%;
      height:38px;
      padding-top:10px;
      // background-color: #F5F7FA;
      color: #F5F7FA;
      // vertical-align: middle;
      text-align: center;
      border: 1px solid #DCDFE6;
      border-radius: 4px;
    }
    .in_content{
      display: inline-block;
      width:75%;
    }
  }
}
.content-body{
  height:89vh;
  background-color: #558FC4;
  text-align: left;
  .chart-div{
    height: 87vh;
    margin-left:10px;
    margin-right:10px;
    margin-top:1vh;
    margin-bottom:1vh;
  }
}
</style>
