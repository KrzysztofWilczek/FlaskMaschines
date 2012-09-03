TaskManager = function() {
    
    this.addRequest = null;
    this.statusRequest = null;
    this.statusTimeout = null;
    this.waitTime = 1000;
    
    this.renderTask = function(task) {
        
        if (!task)
        {
            return;
        }
        return '<tr><td>'+task.id+'</td><td>'+task.task_name+'</td><td>'+task.maschine_name+'</td><td class="stage_'+task.stage+'">'+task.stage_name+'</td></tr>';
    }
    
    this.checkStatus = function()
    {
        // If there's some status request in progress then stop
        if (self.statusRequest)
        {
            return;
        }
        
        // Bind new status request
        self.statusRequest = $.get('/status', function(json) {
            
            // Render html view for each task
            tasks_html = '';
            lower_stage = 3;
            $.each(json.current_tasks, function(index, task) {
                if (task.stage < lower_stage)
                {
                    lower_stage = task.stage;
                }
                tasks_html = tasks_html + self.renderTask(task);
            })
        
            // Put tasks view into DOM
            $('#current_tasks_list').children('tbody').html(tasks_html);
        
            self.statusRequest = null;
            // If there is some work to do for maschines then set timeout for checkStatus
            if (lower_stage < 3)
            {
                self.statusTimeout = setTimeout(self.checkStatus, self.waitTime);    
            }
            else {
                self.enableForm();
                
            }
            
        }, 'json')
            .error(function() {
                self.statusRequest = null;
                self.statusTimeout = setTimeout(self.checkStatus, self.waitTime);
            });
        
    }
    
    this.disableForm = function()
    {
        self.submit.prop('disabled', true);
        self.tasks.prop('disabled', true);
        self.maschines.prop('disabled', true);
    }
    
    this.enableForm = function()
    {
        self.submit.prop('disabled', false);
        self.tasks.prop('disabled', false);
        self.maschines.prop('disabled', false);
        
    }
    
    this.sendAddTask = function()
    {
        var action = $('#tasksForm').attr('action');
        // New task can't be added becourse old one is still in progress
        if (self.addRequest)
        {
            return;
        }
        
        self.addRequest = $.post(action, $('#tasksForm').serialize(), function(json) {
            // New task has been added, so bind recursive check status method
            if (json.status)
            {
                self.disableForm();
                self.checkStatus();
            }
            self.addRequest = null;
        }, 'json')
            .error(function() { self.addRequest = null; });
        
    }
    
    this.validateForm = function()
    {
        return true;
        
    }
    
    // Initialize TaskManager, bind all main DOM elementes 
    this.init = function()
    {
        
        if ($('#sendTask').length == 0)
        {
            console.error('No submit button in task manager form');
        }
        self.submit = $('#sendTask');
        
        self.submit.click(function(event) {
            event.preventDefault();
            if (self.validateForm())
            {
                self.sendAddTask();
            }
        });
        if ($('.task').length == 0)
        {
            console.error('There isn\'t any defined task');
        }
        self.tasks = $('.task');
        if ($('.maschine') == 0)
        {
            console.error('There isn\'t any defined maschine');
        }
        self.maschines = $('.maschine');
        
    }
    
    self = this;
    self.init();
    
}

$(document).ready(function () {
    
    if ($('#tasksForm').length)
    {
        if (!document.manager)
        {
            document.manager = new TaskManager();
        }
    }
});