import { Injectable } from "@angular/core"
import { ComponentLifecycleEventEmitter, TupleGenericAction } from "@synerty/vortexjs"
import {
    BalloonMsgService,
    Sound,
    ISound,
    TitleService,
    BalloonMsgLevel,
    BalloonMsgType
} from "@synerty/peek-plugin-base-js"
import { TaskTuple } from "../tuples/TaskTuple"
import { inboxPluginName } from "../plugin-inbox-names"
import { PrivateInboxTupleProviderService } from "./private-inbox-tuple-provider.service"

/**  Root Service
 *
 * This service will be loaded by peek-mobile when the app loads.
 * There will be one instance of it, and it be around for the life of the app.
 *
 * Configure this in plugin_package.json
 */
@Injectable()
export class PluginInboxRootService extends ComponentLifecycleEventEmitter {
    private tasks: TaskTuple[] = []
    private alertSound: ISound
    
    constructor(
        private balloonMsg: BalloonMsgService,
        private titleService: TitleService,
        private tupleService: PrivateInboxTupleProviderService
    ) {
        super()
        
        try {
            this.alertSound = new Sound("/assets/peek_plugin_inbox/alert.mp3")
        }
        catch (e) {
            console.log(`Failed to load sound : ${e}`)
            this.alertSound = null
        }
        
        // Subscribe to the tuple events.
        this.tupleService.taskTupleObservable()
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: TaskTuple[]) => {
                // Make sure we have the latest flags, to avoid notifying the user again.
                let existingTasksById = {}
                
                for (let task of this.tasks) {
                    existingTasksById[task.id] = task
                }
                
                for (let task of tuples) {
                    let existingTask = existingTasksById[task.id]
                    if (existingTask == null)
                        continue
                    
                    task.stateFlags = (task.stateFlags | existingTask.stateFlags)
                    
                    task.notificationSentFlags =
                        (task.notificationSentFlags | existingTask.notificationSentFlags)
                }
                
                // Now we can set the tasks
                this.tasks = tuples
                
                let notCompletedCount = 0
                for (let task of this.tasks) {
                    notCompletedCount += task.isCompleted() ? 0 : 1
                }
                
                this.titleService.updateButtonBadgeCount(inboxPluginName,
                    notCompletedCount === 0 ? null : notCompletedCount)
                
                let updateApplied = this.processNotifications()
                    || this.processDeletesAndCompletes()
                
                if (updateApplied) {
                    // Update the cached data
                    this.tupleService.tupleDataOfflineObserver.updateOfflineState(
                        this.tupleService.taskTupleSelector, this.tasks)
                }
            })
        
    }
    
    // -------------------------
    // State update methods from UI
    public taskSelected(taskId: number) {
        this.addTaskStateFlag(taskId, TaskTuple.STATE_SELECTED)
    }
    
    public taskActioned(taskId: number) {
        this.addTaskStateFlag(taskId, TaskTuple.STATE_ACTIONED)
    }
    
    private addTaskStateFlag(
        taskId: number,
        stateFlag: number
    ) {
        let filtered = this.tasks.filter(t => t.id === taskId)
        if (filtered.length === 0) {
            // This should never happen
            return
        }
        
        let thisTask = filtered[0]
        this.sendStateUpdate(thisTask, stateFlag, null)
        this.processDeletesAndCompletes()
        
        // Update the cached data
        this.tupleService.tupleDataOfflineObserver.updateOfflineState(
            this.tupleService.taskTupleSelector, this.tasks)
    }
    
    /** Process Delegates and Complete
     *
     * This method updates the local data only.
     * Server side will apply these updates when it gets state flag updates.
     */
    private processDeletesAndCompletes(): boolean {
        let updateApplied = false
        
        let tasksSnapshot = this.tasks.slice()
        for (let task of tasksSnapshot) {
            
            let autoComplete = task.autoComplete & task.stateFlags
            let isAlreadyCompleted = TaskTuple.STATE_COMPLETED & task.stateFlags
            if (autoComplete && !isAlreadyCompleted) {
                task.stateFlags = (TaskTuple.STATE_COMPLETED | task.stateFlags)
                updateApplied = true
            }
            
            // If we're in the state where we should delete, then remove it
            // from our tasks.
            if (task.autoDelete & task.stateFlags) {
                let index = this.tasks.indexOf(task)
                if (index > -1) {
                    this.tasks.splice(index, 1)
                }
                updateApplied = true
            }
        }
        
        return updateApplied
    }
    
    private processNotifications(): boolean {
        let updateApplied = false
        
        for (let task of this.tasks) {
            let notificationSentFlags = 0
            let newStateMask = 0
            
            if (task.isNotifyBySound() && !task.isNotifiedBySound()) {
                
                notificationSentFlags = (
                    notificationSentFlags | TaskTuple.NOTIFY_BY_DEVICE_SOUND)
                
                try {
                    const optionalPromise = this.alertSound && this.alertSound.play()
                    if (optionalPromise != null) {
                        optionalPromise
                            .catch(err => {
                                console.log(`Failed to play alert sound\n${err}`)
                            })
                    }
                }
                catch (e) {
                    console.log(`Error playing sound: ${e.toString()}`)
                }
            }
            
            if (task.isNotifyByPopup() && !task.isNotifiedByPopup()) {
                this.showMessage(BalloonMsgType.Fleeting, task)
                notificationSentFlags = (
                    notificationSentFlags | TaskTuple.NOTIFY_BY_DEVICE_POPUP)
            }
            
            if (task.isNotifyByDialog() && !task.isNotifiedByDialog()) {
                this.showMessage(BalloonMsgType.Confirm, task)
                    .then(() => {
                        this.sendStateUpdate(task,
                            TaskTuple.STATE_DIALOG_CONFIRMED,
                            0
                        )
                    })
                    .catch(err => {
                        let e = `Inbox Dialog Error\n${err}`
                        console.log(e)
                        this.balloonMsg.showError(e)
                    })
                
                notificationSentFlags = (
                    notificationSentFlags | TaskTuple.NOTIFY_BY_DEVICE_DIALOG)
            }
            
            if (!task.isDelivered()) {
                newStateMask = (newStateMask | TaskTuple.STATE_DELIVERED)
            }
            
            if (notificationSentFlags || newStateMask) {
                updateApplied = true
                
                this.sendStateUpdate(task,
                    newStateMask,
                    notificationSentFlags
                )
            }
        }
        
        return updateApplied
    }
    
    private showMessage(
        type_: BalloonMsgType,
        task: TaskTuple
    ): Promise<null> {
        let level: BalloonMsgLevel | null = null
        
        switch (task.displayPriority) {
            case TaskTuple.PRIORITY_SUCCESS:
                level = BalloonMsgLevel.Success
                break
            
            case TaskTuple.PRIORITY_INFO:
                level = BalloonMsgLevel.Info
                break
            
            case TaskTuple.PRIORITY_WARNING:
                level = BalloonMsgLevel.Warning
                break
            
            case TaskTuple.PRIORITY_DANGER:
                level = BalloonMsgLevel.Error
                break
            
            default:
                throw new Error(`Unknown priority ${task.displayPriority}`)
            
        }
        
        let dialogTitle = `New ${task.displayAsText()}`
        let desc = task.description ? task.description : ""
        let msg = `${task.title}\n\n${desc}`
        
        return this.balloonMsg.showMessage(
            msg,
            level,
            type_, {
                "confirmText": "Ok",
                "dialogTitle": dialogTitle,
                "routePath": task.routePath
            })
    }
    
    private sendStateUpdate(
        task: TaskTuple,
        stateFlags: number | null,
        notificationSentFlags: number | null
    ) {
        let action = new TupleGenericAction()
        action.key = TaskTuple.tupleName
        action.data = {
            id: task.id,
            stateFlags: stateFlags,
            notificationSentFlags: notificationSentFlags
        }
        this.tupleService.tupleOfflineAction.pushAction(action)
            .catch(err => alert(err))
        
        if (stateFlags != null) {
            task.stateFlags = (task.stateFlags | stateFlags)
        }
        
        if (notificationSentFlags != null) {
            task.notificationSentFlags =
                (task.notificationSentFlags | notificationSentFlags)
        }
    }
}
