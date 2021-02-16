resource=[
    "//cdn.jsdelivr.net/raphael/2.1.0/raphael-min.js",
    "//cdn.jsdelivr.net/justgage/1.0.1/justgage.min.js"
   ]
   
   //add scripts to head
   $.getScript(resource[0],function(){
    $.getScript(resource[1],init)
   })
   
   
   
   ////////////////////////////////gauge 1
   init = function(){
     var g = new JustGage({
       id: "gauge1", 
       value: "10", 
       min: 0,
       max: 50,
       title: "Seemek"
     });  
   
     //refresh gauge when calcvalue changes
     $(calcValue1).one('DOMSubtreeModified',function(){
       g.refresh($(this).text())
     })
   
   ////////////////////////////////gauge 2
     
       var g = new JustGage({
       id: "gauge2", 
       value: "22", 
       min: 0,
       max: 50,
       title: "Maabadot"
     });  
   
     //refresh gauge when calcvalue changes
     $(calcValue2).one('DOMSubtreeModified',function(){
       g.refresh($(this).text())
     })
   
     
   ////////////////////////////////gauge 3
     
       var g = new JustGage({
       id: "gauge3", 
       value: "33", 
       min: 0,
       max: 50,
       title: "Shetach-G"
     });  
   
    //refresh gauge when calcvalue changes
     $(calcValue3).one('DOMSubtreeModified',function(){
     g.refresh($(this).text())
    })
   
   }