function err_message_quietly(msg, f) {
    $.layer({
        title: false,
        closeBtn: false,
        time: 2,
        dialog: {
            msg: msg
        },
        end: f
    });
}

function ok_message_quietly(msg, f) {
    $.layer({
        title: false,
        closeBtn: false,
        time: 1,
        dialog: {
            msg: msg,
            type: 1
        },
        end: f
    });
}

function my_confirm(msg, btns, yes_func, no_func) {
    $.layer({
        shade: [ 0 ],
        area: [ 'auto', 'auto' ],
        dialog: {
            msg: msg,
            btns: 2,
            type: 4,
            btn: btns,
            yes: yes_func,
            no: no_func
        }
    });
}

function handle_quietly(json, f) {
    if (json.msg.length > 0) {
        err_message_quietly(json.msg);
    } else {
        ok_message_quietly("successfully:-)", f);
    }
}

// - business function -
function all_select() {
    var boxes = $("input[type=checkbox]");
    for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked="checked";
    }
}

function reverse_select() {
    var boxes = $("input[type=checkbox]");
    for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) {
            boxes[i].checked=""
        } else {
            boxes[i].checked="checked";
        }
    }
}

function batch_solve() {
    var boxes = $("input[type=checkbox]");
    var ids = [];
    for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) {
            ids.push($(boxes[i]).attr("alarm"));
        }
    }

    $.ajax({
        url: '/api/alarms/' + ids.join(','),
        method: 'DELETE',
        success: function(rst) {
            if (rst.result === 'success') {
                location.reload();
            } else {
                alert(rst.reason);
            }
        },
    });
}

function solve(id) {
    $.ajax({
        url: '/api/alarms/' + id,
        method: 'DELETE',
        success: function(rst) {
            if (rst.result === 'success') {
                location.reload();
            } else {
                alert(rst.reason);
            }
        },
    });
}

$(function() {
  $.ajax({
    url: '/api/alarms',
    method: 'GET',
    success: function(resp) {
      var items = [];
      // var rst = JSON.parse(resp);
      resp.alarms.map(function(alarm) {
        items.push(`
          <div class="alarm">
              <a name="${alarm.id}"></a>
              <input type="checkbox" alarm="${alarm.id}">
              [P${alarm.level} #${alarm.step}/${alarm.max_step}] ${alarm.title}<br>
              <span style="padding-left:17px;">${alarm.text}</span>
              <span class="orange">${alarm.formatted_time}</span>
              <span class="gray">[</span>
              <!--<a href="#" target="_blank">config</a>
              <span class="cut-line">¦</span>-->
              <a href="javascript:solve('${alarm.id}');">Resolve</a>
              <span class="gray">]</span>
          </div>
          <hr>
        `);
      });
      $('#alarms').html(items.join(''));
    },
  });
});
