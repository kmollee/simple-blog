//@+leo-ver=5-thin
//@+node:lee.20150113062053.6: * @file Listdetail.js
(function($) {
    $.fn.flash_message = function(options) {

      options = $.extend({
        text: 'Done',
        time: 1000,
        how: 'before',
        class_name: ''
      }, options);

      return $(this).each(function() {
        if( $(this).parent().find('.flash_message').get(0) )
          return;

        var message = $('<span />', {
          'class': 'flash_message ' + options.class_name,
          text: options.text
        }).hide().fadeIn('fast');

        $(this)[options.how](message);

        message.delay(options.time).fadeOut('normal', function() {
          $(this).remove();
        });

      });
    };
})(jQuery);
    function get_task(task_element){
        return task_element.closest('.task');
    }
    function get_task_status(task){
        // check is complete or not
        var complete = task.attr('completed');
        var priority = task.attr('priority');
        return {'completed':complete, 'priority':(priority)};
    }
    function insertTask(task){
        var task_status = get_task_status(task);
        console.log(task_status.completed);

        // after click, completed will be oppsite
        task_status.completed = task_status.completed == 'True'? false:true;
        console.log(task_status.completed);
        task.attr('completed', function(){
            if(task_status.completed){
                return 'True';
            }
            return 'False';
        });
        if(task_status.completed){
            //select completed task
            var targetTask = $(".task[completed='True']");
        }
        else{
            //select incompleted task
            var targetTask = $(".task[completed='False']");
        }

        targetTask = targetTask.filter(function(){
                if ($(this).attr('priority') == task_status.priority)
                    return $(this);
            });

        console.log('here is select result:', targetTask);

        if(targetTask.size()){
            console.log("incomeingggggg");
            task.insertAfter(targetTask.filter(":last"));
        }
        else{
            console.log("here is gogging");
            if(task_status.completed){
                $('.tasks').append(task);
            }
            else{
                $('.tasks').prepend(task);
            }
        }
    }

    // make all task-content, first user saw is invisible
    $('.task-content').toggle();
    // if user click checkbox
    $('body').on('click', '.togglebtn', function(){
        var url = $(this).attr('href');
        var task = get_task($(this));
        $.ajax({
            url:url,
            type:'POST',
            success:function(data){
                var msg = data['result'];
                $('#msg').flash_message({
                    text: msg,
                    how: 'append'
                });
                task = task.detach();
                insertTask(task);
            },
            error:function(xhr, errmsg, err){
                $('#data').flash_message({
                    text: "Oops! We have encountered an error: "+errmsg,
                    how: 'append'
                });
            }
        });
    });
    // if any task-anchor is clicked, togggle it's content
    $('body').on('click', '.task-anchor', function(event){
        // stop prevent action
        event.preventDefault();
        //console.log($(this));
        // get the task element
        var task = $(this).closest( ".task" );
        // get the child task-content
        var task_content = task.children('.task-content');
        // make it toogle, if it's open, then close it
        // if it's close, then open it
        task_content.toggle();
    });

    $('body').on('click', '.deletebtn', function(event){
        // stop prevent action
        event.preventDefault();
        var url=$(this).attr('href');
        var task = get_task($(this));
        $.ajax({
            url:url,
            type:'POST',
            success:function(data){
                $('#msg').flash_message({
                    text: "delete success",
                    how: 'append'
                });
                task.remove();
            },
            error:function(xhr, errmsg, err){
                $('#data').flash_message({
                    text: "Oops! We have encountered an error: "+errmsg,
                    how: 'append'
                });
            }
        });
    });

    $(document).ready(function(){
        $('#id_note').wysihtml5({
              toolbar: {
                "font-styles": true, //Font styling, e.g. h1, h2, etc. Default true
                "emphasis": true, //Italics, bold, etc. Default true
                "lists": true, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
                "html": true, //Button which allows you to edit the generated HTML. Default false
                "link": true, //Button to insert a link. Default true
                "image": true, //Button to insert an image. Default true,
                "color": true, //Button to change color of font
                "blockquote": true, //Blockquote
                "size": "sm" //default: none, other options are xs, sm, lg
              }
        });
    });
//@-leo
