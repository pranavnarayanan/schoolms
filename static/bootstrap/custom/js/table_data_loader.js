
  _current_page = 1;
  _total_pages = 1;
  _total_records = 10;

  _page = 1;
  _records_count =10;
  _search = null;


  var loadingIcon = '<i class="fa fa-refresh fa-spin"></i>';

  function getJsonResponse(paramURL, page, pageRowCount,searchKeyword){
      $("#page_loading_div").addClass("overlay");
      $("#page_loading_div").html(loadingIcon);

      return $.ajax({
           url:paramURL,
           data:({
               "page":page,
               "page_row_count":pageRowCount,
               "search_keyword":searchKeyword
           }),
           type:"POST",
           error:function(data){
               $("#page_loading_div").addClass("overlay");
               $("#page_loading_div").html("<label>"+data.responseText.substr(0, 2000)+"</lable>");
           }
       });
  }

  function search(){
      _search = $("#table_search").val();
      if (_search == ""){
          _search = null;
      }
      _page = 1;
      loadData(_page,_records_count,_search);
  }

  function clearFilter(){
    $("#table_search").val("");
    if(_search != null){
      _page = 1;
      _search = null;
      loadData(_page,_records_count,_search);
    }
  }


  function pagination(action){
      if(action == "backward"){
          if(_page > 1){
            _page = _page-1;
            loadData(_page,_records_count,_search);
          }
      }

      else if(action == "forward"){
          if(_page < _total_pages) {
              _page = _page + 1;
              loadData(_page, _records_count, _search);
          }
      }
  }
