

import {inboxTuplePrefix} from "../plugin-inbox-names";
import {Tuple, addTupleType} from "@synerty/vortexjs";

@addTupleType
export class TaskActionTuple extends Tuple {

    static readonly tupleName =  inboxTuplePrefix + 'TaskAction';

    id :number;
    taskId :number;
    title :string;
    confirmMessage :string;

    constructor() {
        super(TaskActionTuple.tupleName);
    }
}