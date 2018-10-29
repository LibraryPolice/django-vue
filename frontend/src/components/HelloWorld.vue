
<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
      <el-col :span="12">
    <el-card >
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
        <!--</el-table-column>-->
          <!--<el-table-column prop="id" label="label" min-width="100">-->
        <!--<template scope="scope"> {{scope.row[0]}} </template>-->
        </el-table-column>
         <el-table-column prop="id" label="输入想要检索的内容" min-width="100">
        <template scope="scope"> <el-input v-model="search_list[scope.row.index].input"> </el-input></template>
        </el-table-column>
    </el-table>
        <el-col :span="12"><el-button @click="index_search()">查询 </el-button></el-col>
      <el-col :span="12"><el-button @click="add_search()">添加条件 </el-button></el-col>
      <!--<el-table :data="search_list" border>-->
        <!--<template scope="scope">-->
          <!--{{scope.row}}-->
       <!--<el-col :offset='2' :span="10"><el-input v-model="input"> </el-input></el-col>-->
      <!--<el-col :span="6">-->
      <!--<el-select  v-model="search_header" placeholder="请选择">-->
          <!--<el-option-->
            <!--v-for="item in index_header"-->
            <!--:key="item[1]"-->
            <!--:label="item[1]"-->
            <!--:value="item[0]">-->
          <!--</el-option>-->
        <!--</el-select>-->
        <!--</el-col>-->
        <!--</template>-->
      <!--</el-table>-->
      <!--&lt;!&ndash;<el-col :span="3"><el-button @click="index_search()">查询 </el-button></el-col>&ndash;&gt;-->
      <!--<el-col :span="3"><el-button @click="index_search()">添加条件 </el-button></el-col>-->
    </el-card>
      <el-card align="center">
         <el-table :data="booklist.slice((currentPage-1)*pagesize,currentPage*pagesize)" border>
        <el-table-column prop="id" label="label" min-width="100">
        <template scope="scope"> {{scope.row}} </template>
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
        </el-col>


      <el-col :span="12">

    <el-card :span="12">

       <el-upload
          enctype="multipart/form-data"
          class="upload-demo"
          accept=".csv"
          action="http://39.105.79.167/api/upload_file"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          :on-success="handleSuccess"
          :limit="1"
          :on-exceed="handleExceed"
          :file-list="fileList"><el-button    size="small" type="primary">上传自己的csv文件并建立索引</el-button>
          </el-upload>
      <el-tag>默认使用神奇宝贝资料库.csv</el-tag>
      <el-row>
          <el-header>倒排索引表预览</el-header>
          <el-select @change=change_label v-model="chosen_header" placeholder="请选择">
          <el-option
            v-for="item in index_header"
            :key="item[1]"
            :label="item[1]"
            :value="item[0]">
          </el-option>
        </el-select>
        </el-row>
      <el-table :data="indexlist.slice((currentPage2-1)*pagesize2,currentPage2*pagesize2)" border>
        <el-table-column prop="id" label="label" min-width="100">
        <template scope="scope"> {{scope.row[0]}} </template>
        </el-table-column>


        <el-table-column prop="id" label="index" min-width="100">
        <template scope="scope"> {{scope.row[1]}} </template>
        </el-table-column>
      </el-table>
<el-pagination

      @size-change="handleSizeChange2"
      @current-change="handleCurrentChange2"
      :current-page="currentPage2"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pagesize2"
      layout="total, sizes, prev, pager, next, jumper"
      :total=parseInt(indexlist.length)>
    </el-pagination>
    </el-card>
      </el-col>
      </div>
</template>

<script>
  import Vue from 'vue'
export default {
  name: 'HelloWorld',
  data () {
    return {
      search_list:[{'index':0,'header':'','input':''
      }],
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
      msg: 'Welcome to the Assignment-1'
    }
  },
  mounted(){
     this.axios.get(' http://39.105.79.167/api/init_book', {
      })
    .then((res) => {

        let data = res.data.data;
        console.log(res.data.header)
        for(let index in res.data.header){
          this.index_header.push([index,res.data.header[index]])
        }
        console.log(this.index_header)
         for(let index in data){
              let mid_index = []
            for(let i in data[index]) {
              if (i != "" && i != " " && i != null) {
                mid_index.push([i, data[index][i]]);
              }
            }
              this.big_indexlist.push(mid_index)
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
    index_search(){
      let search_header=''
      let search_input=''
       for(let i in this.search_list){
         search_header+=this.search_list[i]['header']+"?"
         search_input+=this.search_list[i]['input']+"?"
       }
      console.log(search_header)
     this.axios.get(' http://39.105.79.167/api/show_books', {

      params: {
        "search_header": search_header,
        "search_input":search_input
      }})
    .then((res) => {
      this.currentPage=1,
      this.booklist=[]
      for (let  par_index in res.data.list){
        let row=""
        for(let row_index in res.data.list[par_index]){
          row+=res.data.list[par_index][row_index]+"  "
        }

        this.booklist.push(row)
      }
          })
    .catch((res) => {
    });
    },
  },
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
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

