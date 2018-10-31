
<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
<el-row>
      <el-col :offset='6' :span="12">
      <el-input v-model="main_search"> </el-input>
        </el-col>

      <el-col :span="3">
           <el-button @click="mix_search()">搜索</el-button>
        </el-col>
      <el-col :span="3">
          <el-button type="info" plain @click=" max_search_selected()">高级搜索</el-button>
        </el-col>
</el-row>

    <el-card v-show="max_search">
       <el-table :data="search_list" border>
        <el-table-column prop="id" label="选择需要检索的项" min-width="100">
        <template scope="scope">
          <el-select  v-model="search_list[scope.row.index].header" placeholder="请选择">
          <el-option
            v-for="item in index_header"
            :key="item[1]"
            :label="item[1]"
            :value="item[0]">
          </el-option>
        </el-select>
        </template>
        </el-table-column>
         <el-table-column prop="id" label="输入想要检索的内容" min-width="100">
        <template scope="scope"> <el-input v-model="search_list[scope.row.index].input"> </el-input></template>
        </el-table-column>
    </el-table>
        <el-col :span="12"><el-button @click="index_search()">查询 </el-button></el-col>
      <el-col :span="12"><el-button @click="add_search()">添加条件 </el-button></el-col>
    </el-card>


      <el-card align="center" v-show="is_searched">
        <el-table :data="booklist.slice((currentPage-1)*pagesize,currentPage*pagesize)" border>
          <el-table-column prop="id" label="名字" show-overflow-tooltip min-width="100">
          <template scope="scope">
             <a :href="'https://wiki.52poke.com/wiki/'+scope.row[0]"
            target="_blank"
            class="buttonText">{{scope.row[0]}}</a>
             </template>
          </el-table-column>
           <el-table-column prop="id" label="基本信息" show-overflow-tooltip min-width="100">
          <template scope="scope"> {{scope.row[1]}} </template>
          </el-table-column>
           <el-table-column prop="id" label="出场信息" show-overflow-tooltip  min-width="100">
          <template scope="scope"> {{scope.row[2]}} </template>
          </el-table-column>
            <el-table-column prop="id" label="关键属性" show-overflow-tooltip min-width="100">
          <template scope="scope"> {{scope.row[3]}} </template>
            </el-table-column>


    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total=parseInt(booklist.length)>
    </el-pagination>
    </el-card>

      <!--<el-col :span="12">-->

    <!--<el-card :span="12">-->

       <!--<el-upload-->
          <!--enctype="multipart/form-data"-->
          <!--class="upload-demo"-->
          <!--accept=".csv"-->
          <!--:action="UploadServer"-->
          <!--:on-preview="handlePreview"-->
          <!--:on-remove="handleRemove"-->
          <!--:before-remove="beforeRemove"-->
          <!--:on-success="handleSuccess"-->
          <!--:limit="1"-->
          <!--:on-exceed="handleExceed"-->
          <!--:file-list="fileList"><el-button    size="small" type="primary">上传自己的csv文件并建立索引</el-button>-->
          <!--</el-upload>-->
      <!--<el-tag>默认使用神奇宝贝资料库.csv</el-tag>-->
      <!--<el-row>-->
          <!--<el-header>倒排索引表预览</el-header>-->
          <!--<el-select @change=change_label v-model="chosen_header" placeholder="请选择">-->
          <!--<el-option-->
            <!--v-for="item in index_header"-->
            <!--:key="item[1]"-->
            <!--:label="item[1]"-->
            <!--:value="item[0]">-->
          <!--</el-option>-->
        <!--</el-select>-->
        <!--</el-row>-->
      <!--<el-table :data="indexlist.slice((currentPage2-1)*pagesize2,currentPage2*pagesize2)" border>-->
        <!--<el-table-column prop="id" label="label" min-width="100">-->
        <!--<template scope="scope"> {{scope.row[0]}} </template>-->
        <!--</el-table-column>-->


        <!--<el-table-column prop="id" label="index" min-width="100">-->
        <!--<template scope="scope"> {{scope.row[1]}} </template>-->
        <!--</el-table-column>-->
      <!--</el-table>-->
<!--<el-pagination-->

      <!--@size-change="handleSizeChange2"-->
      <!--@current-change="handleCurrentChange2"-->
      <!--:current-page="currentPage2"-->
      <!--:page-sizes="[10, 20, 30, 40]"-->
      <!--:page-size="pagesize2"-->
      <!--layout="total, sizes, prev, pager, next, jumper"-->
      <!--:total=parseInt(indexlist.length)>-->
    <!--</el-pagination>-->
    <!--</el-card>-->
      <!--</el-col>-->
      </div>
</template>

<script>
  import Vue from 'vue'
  // import global_ from 'Global'
export default {
  name: 'HelloWorld',
  data () {
    return {
      max_search: false,
      is_searched :false,
      main_search:'',
      UploadServer:this.GLOBAL.server+"/api/upload_file",
      search_list:[{'index':0,'header':'','input':''
      }],
      server:this.GLOBAL.server,
      search_int:0,
      search_header:'',
      chosen_header:'',
      index_header:[],
      currentPage:1,
        pagesize:10,
      currentPage2:1,
        pagesize2:10,
     fileList: [],
     booklist: [],
      big_indexlist:[],
      indexlist:[],
      input:"",
      msg: '精灵宝可梦搜索'
    }
  },
  mounted(){
     this.axios.get(this.GLOBAL.server+'/api/init_book', {
      })
    .then((res) => {

        let data = res.data.data;
        for(let index in res.data.header){
          this.index_header.push([index,res.data.header[index]])
        }
        this.chosen_header=res.data.header[0]
        this.indexlist=this.big_indexlist[0]
    })
    .catch((res) => {
    });
  },
  methods:{
    add_search(){
      let search=[]
      this.search_int+=1
      this.search_list.push(search)
      Vue.set(this.search_list[this.search_int],'index',this.search_int)
      Vue.set(this.search_list[this.search_int],'header',this.search_int)
      Vue.set(this.search_list[this.search_int],'input',this.search_int)
      console.log(this.search_list)
    },
    change_label(){
      this.indexlist=this.big_indexlist[this.chosen_header]
    },
    handleSizeChange(val) {
        this.pagesize = val;
      },
//        console.log(`每页 ${val} 条`);
      handleCurrentChange(val) {
        this.currentPage = val;
      },
    handleSizeChange2(val) {
        this.pagesize2 = val;
      },
//        console.log(`每页 ${val} 条`);
      handleCurrentChange2(val) {
        this.currentPage2= val;
      },
    handleSuccess(res,file){
      this.index_header=[]
      this.big_indexlist=[]
      this.currentPage2=1
        let data = res.data;
        for(let index in res.header){
          this.index_header.push([index,res.header[index]])
        }
         for(let index in data){
              let mid_index = []
            for(let i in data[index]) {
              if (i != "" && i != " " && i != null) {
                mid_index.push([i, data[index][i]]);
              }
            }
              this.big_indexlist.push(mid_index)
          }
        this.chosen_header=res.header[0]
        this.indexlist=this.big_indexlist[0]
    },
    handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 1 个文件`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
    mix_search(){
      this.is_searched=true
      this.axios.get(this.GLOBAL.server+'/api/show_books', {
      params: {
        "search_header": " ",
        "search_input":this.main_search,
        "search_mode":'0'
      }})
        .then((res) => {
          this.currentPage=1
            if(res.data.list.length != 0){

                 this.booklist=res.data.list}
}
           )
        .catch((res) => {
        });
    },
    max_search_selected(){
       this.max_search=!this.max_search
      console.log(this.max_search)
    },
    index_search(){
      this.is_searched = true
      let search_header=''
      let search_input=''
       for(let i in this.search_list){
         search_header+=this.search_list[i]['header']+"?"
         search_input+=this.search_list[i]['input']+"?"
       }
      console.log(search_header)
     this.axios.get(this.GLOBAL.server+'/api/show_books', {

      params: {
        "search_header": search_header,
        "search_input":search_input,
        "search_mode":'1'
      }})
    .then((res) => {
          this.currentPage=1
               if(res.data.list.length != 0){
          this.booklist=res.data.list}
          })
        .catch((res) => {
        });
        },
  },
}
</script>
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

