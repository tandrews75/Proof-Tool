function get_total_proofline_form_count(){
    return document.getElementsByClassName('proofline_set').length;
}

function get_total_formset_count_in_manager(){
    return parseInt(document.getElementById('id_proofline_set-TOTAL_FORMS').value)
}

function set_total_formset_count_in_manager(value){
    document.getElementById('id_proofline_set-TOTAL_FORMS').setAttribute('value', value);
}


function get_proofline_form_id_from_object_id(oObj){
    return parseInt(oObj.id.replace(/[^0-9]/g, ""))
}

function init_proof(){
    if (get_total_formset_count_in_manager() == 0) {
        append_new_form_in_proofline_formset(0)
    }
}

function change_proofline_form_id(old_id, new_id){
    const targeted_element = document.getElementById('proofline_set-'+old_id)
    if (targeted_element != null) {
        document.getElementById('proofline_set-' + old_id).setAttribute('id', `proofline_set-${new_id}`)
        const fields = ['id', 'DELETE', 'line_no', 'formula', 'rule'];
        fields.forEach(function (field) {
            document.getElementById('id_proofline_set-' + old_id + '-' + field).setAttribute('name', `proofline_set-${new_id}-${field}`)
            document.getElementById('id_proofline_set-' + old_id + '-' + field).setAttribute('id', `id_proofline_set-${new_id}-${field}`)
        })
        document.getElementById('id-form-btn-insert-row-' + old_id).setAttribute('id', `id-form-btn-insert-row-${new_id}`)
        document.getElementById('id-form-btn-delete-row-' + old_id).setAttribute('id', `id-form-btn-delete-row-${new_id}`)
    }
}

function push_down_proofline_forms(from_index){
    const last_form_element_id = get_total_formset_count_in_manager() - 1;
    for (let i = last_form_element_id; i >= from_index; i--) {
        change_proofline_form_id(i, i+1)
    }
}

function pull_up_proofline_forms(to_index){
    const last_form_element_id = get_total_formset_count_in_manager() - 1;
    for (let i = to_index+1; i <= last_form_element_id; i++) {
        change_proofline_form_id(i, i-1)
    }
}

function add_proofline_form(oObj){
    append_new_form_in_proofline_formset(get_proofline_form_id_from_object_id(oObj)+1)
}

function remove_proofline_form(oObj){
    remove_existing_form_from_proofline_fomrset(get_proofline_form_id_from_object_id(oObj))
}

function remove_new_proofline_form(oObj){
    remove_new_form_from_proofline_fomrset(get_proofline_form_id_from_object_id(oObj))
}

function append_new_form_in_proofline_formset(index){
    push_down_proofline_forms(index)

    const emptyFormElement = document.getElementById('empty-form').cloneNode(true)
    emptyFormElement.setAttribute("class", 'proofline_set')
    emptyFormElement.setAttribute("id", `proofline_set-${index}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, index)

    const proof_tbody = document.getElementById('proofline-list')
    const proof_table_row = document.getElementById('proofline_set'+"-"+(index-1))
    if (proof_table_row != null){
        proof_table_row.after(emptyFormElement)
    } else {
        proof_tbody.append(emptyFormElement)
    }
    set_total_formset_count_in_manager(get_total_formset_count_in_manager()+1)
}

function remove_existing_form_from_proofline_fomrset(index) {
    document.getElementById('id_proofline_set-' + index + '-DELETE').setAttribute("checked", "true")
    document.getElementById('proofline_set-' + index).hidden = true;
}

function remove_new_form_from_proofline_fomrset(index) {
    document.getElementById('id_proofline_set-' + index + '-DELETE').setAttribute("checked", "true")
    document.getElementById('proofline_set-' + index).remove()
    pull_up_proofline_forms(index)
    set_total_formset_count_in_manager(get_total_formset_count_in_manager()-1)
}

function replaceCharacter(ev) {
    console.log(document.getElementById(ev.id));
    let txt = document.getElementById(ev.id).value;
    console.log(txt);

    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    txt = txt.replace("\\iff", "↔");
    txt = txt.replace("\\contradiction", "⊥");
    document.getElementById(ev.id).value = txt;
}