function dateToNumber(input_val){
  let temp;
  let x = 31; //coefficient for days in a month
  let month;

  if(input_val.length <= 6){
    temp = input_val.split('.');
    month = parseInt(temp[1])
    switch(month){ //adjusting days in a month
      case 2:
        x = 28;
      case 4:
      case 6:
      case 9:
      case 11:
        x = 30;
    }
    input_val = parseInt(temp[0]) + (month * x); //converting date to days number
  }else if(input_val.includes("aktualizováno")){
    input_val = 0;
  }else{
    input_val = 1;
  }
  return input_val
}
function salaryAverage(input_val){
  let temp;
  temp = input_val.replace(/\s/g, '');
  if(temp != "n/a"){
    temp = temp.replace(/&nbsp;/g,'')
    temp = temp.replace(/Kč/gi,'')
    if(temp.includes("–‍")){
      temp = temp.split('‍–‍');
      temp = (parseInt(temp[0]) + parseInt(temp[1]))/2;
    }
  }else{
    temp = 0;
  }
  return temp;
}

function sortTable(col) {
  let table,rows,row,row2,row_c,row_c2,run,counter,sort_dir,row_val,row2_val;
  table = document.getElementById("job_table");
  rows = table.rows;
  run = true;
  counter = 0;
  sort_dir = "asc";
  document.querySelector(".loader").classList.add("loader_vis"); // add "loader_vis" class to show loading animation

  setTimeout(() => { //timeout to allow browser to update and show loading animation
    while (run) {
      run = false;
      for (let i = 1; i < rows.length - 1; i++) {
        row_c = rows[i].getElementsByTagName("TD")[col];
        row_c2 = rows[i + 1].getElementsByTagName("TD")[col];
        row = rows[i];
        row2 = rows[i + 1];
        row_val = row_c.innerHTML.toLowerCase();
        row2_val = row_c2.innerHTML.toLowerCase();
        temp = "";
        if (col == 3) {
          row_val = dateToNumber(row_val);
          row2_val = dateToNumber(row2_val);
        }
        if (col == 1) {
          row_val = salaryAverage(row_val);
          row2_val = salaryAverage(row2_val);
        }

        if (row_val < row2_val && sort_dir == "asc") {
          row.parentNode.insertBefore(row2, row);
          run = true;
          counter++;
        } else if (row_val > row2_val && sort_dir == "desc") {
          row.parentNode.insertBefore(row2, row);
          run = true;
          counter++;
        }
      }
      if (counter == 0 && sort_dir == "asc") {
        sort_dir = "desc";
        run = true;
      }
    }
    document.querySelector(".loader").classList.remove("loader_vis");
  }, 0);
}
function loading() {
  if(document.querySelector(".main_form").checkValidity()){
    document.querySelector(".loader").classList.toggle("loader_vis")
  }
}
function loadingCheck() {
  let element = document.querySelector(".loader_vis");
  if( element != null){
    element.classList.remove("loader_vis");
  }
}
