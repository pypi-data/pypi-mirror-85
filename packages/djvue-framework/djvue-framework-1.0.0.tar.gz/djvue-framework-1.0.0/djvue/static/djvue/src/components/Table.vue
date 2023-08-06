<template>
    <div>

        <div v-if="showCreate || showSearch" class="d-flex">
            <b-form-group v-if="showSearch"
                          :label-for="filterId"
                          v-bind="formGroupProps"
                          class="flex-grow-1">
                <b-input-group size="sm">
                    <template v-slot:prepend>
                        <b-input-group-text>
                            <b-icon icon="search"></b-icon>
                        </b-input-group-text>
                    </template>
                    <b-form-input v-model="filter"
                                  type="search"
                                  :id="filterId"
                                  size="sm" placeholder="cerca..."
                                  ref="filter_input"
                                  v-bind="formInputProps">
                    </b-form-input>
                </b-input-group>

            </b-form-group>
            <slot name="djvue_create_button" v-bind:scope="{button: list_api_info.create_button}">
                <component
                           v-if="showCreate"
                           :is="getExtraButtonType(list_api_info.create_button)"
                           v-bind="list_api_info.create_button.props"
                           :operation="eoperation.CREATE"
                           :defaultParams="defaultParams"
                           v-on:dv::object::created="refresh()"
                          >
                </component>
            </slot>
        </div>


        <b-table
            :id="id"
            :items="provider"
            :fields="fields"
            :per-page="perPage"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            :current-page="currentPage"
            :filter="filter"
            :busy="busy"
            ref="table"
            v-on="$listeners"
            v-bind="tableProps">

            <template v-slot:head(checkField)="scope">
                <b-checkbox @change="toggleAllRows" :indeterminate="someRowsSelected"
                            :checked="allRowsSelected"></b-checkbox>
            </template>

            <template v-slot:cell(checkField)="scope">
                <b-checkbox v-model="selectedKeysDict[scope.item[list_api_info.list_select_key]]">
                </b-checkbox>
            </template>

            <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
                <slot :name="slot" v-bind="scope"/>
            </template>

            <template v-slot:cell(djvue_extra_buttons)="scope">
                <slot name="cell(djvue_extra_buttons)" v-bind:scope="scope">
                    <div class="d-flex justify-content-end">
                        <component v-for="button in scope.item.extra_buttons"
                                   :is="getExtraButtonType(button)"
                                   v-bind="button.props"
                                   :key="button.key"
                                   :defaultParams="defaultParams"
                                   @click="$emit('click_extra_button', $event, button.key, scope)"
                                   v-on:dv::object::created="refresh()"
                                   v-on:dv::object::deleted="refresh()"
                                   v-on:dv::object::updated="refresh()">
                            {{ button.props['label'] }}
                        </component>
                    </div>
                </slot>
            </template>

        </b-table>

        <div v-if="showPaginator" class="d-flex justify-content-end">
            <b-pagination
                v-model="currentPage"
                :aria-controls="id"
                :total-rows="totalItems"
                :per-page="perPage"
                ref="pagination"
                v-bind="paginationProps">
            </b-pagination>
        </div>


    </div>
</template>

<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
import ListComponent from "@/components/ListComponent";
import ModalForm from "@/components/ModalForm.vue";
import {EOperation, ExtraButtonType, TableActionInterface, TableField} from "@/interfaces/ApiInfo";
import {BButton} from "bootstrap-vue";
import Form from "@/components/Form.vue";

@Component({
    name: "Table",
    components: {
        ModalForm: ModalForm,
        Form: Form
    }
})
export default class Table extends ListComponent {
    @Prop(Array) protected readonly preFields?: TableField[];
    @Prop(Array) protected readonly postFields?: TableField[];
    @Prop() protected readonly tableProps?: any;
    @Prop() protected readonly formGroupProps?: any;
    @Prop() protected readonly formInputProps?: any;
    @Prop() protected readonly paginationProps?: any;
    eoperation = EOperation;

    private aaa = [{}, {}]

    iii() {
        alert()
    }

    private selectedKeysDict: { [key: string]: boolean; } = {};

    private getExtraButtonType(extraButton: TableActionInterface) {
        switch (extraButton.type) {
            case ExtraButtonType.BUTTON:
                return BButton
            case ExtraButtonType.MODAL:
                return ModalForm
        }
    }

    get filterId() {
        return 'filterInput_' + this.id;
    }

    get showSearch() {
        return this.list_api_info.search_filter.search_fields.length > 0;
    }

    get showCreate() {
        return this.list_api_info.allow_creation;
    }

    @Watch('filter')
    private onChangeFilter() {
        this.currentPage = 1;
    }

    get showPaginator() {
        return this.list_api_info.is_paginated && this.totalItems > this.perPage
    }

    get fields() {

        if (!this.initialized) {
            return [];
        }

        let res: TableField[];
        let keys: string[];

        if (this.list_api_info.list_fields.length == 0) {
            keys = Object.keys(this.list_api_info.fields)
        } else {
            keys = this.list_api_info.list_fields;
        }

        res = keys.map((key: any) => {
            let field = this.list_api_info.fields[key];
            return {
                key: key,
                label: field.label || key,
                sortable: this.list_api_info.ordering_filter.ordering_fields.indexOf(key) > -1
            }
        })

        if (this.list_api_info.list_select_key != '')
            res.unshift({key: 'checkField', label: '', sortable: false});

        if (this.preFields) {
            res = this.preFields.concat(res);
        }

        if (this.postFields) {
            res = res.concat(this.postFields)
        }

        if (this.list_api_info.has_extra_buttons) {
            res = res.concat({key: "djvue_extra_buttons", label: "", sortable: false});
        }

        return res
    }

    provider(ctx: any, cb: any) {
        if (!this.initialized) {
            return []
        }

        this.fetch().then(() => {
                cb(this.items)
            }
        );
        return null;

    }

    get filteredItems() {
        // todo: implementare filtro lato front
        return this.items
    }

    init() {
        (this.$refs['table'] as any).refresh();
    }

    refresh() {
        (this.$refs['table'] as any).refresh();
    }

    get selectedKeys(): string[] {
        return Object.keys(this.selectedKeysDict).filter((key) => {
            return this.selectedKeysDict[key]
        });
    }

    get allRowsSelected(): boolean {
        return this.selectedKeys.length === this.totalItems;
    }

    get someRowsSelected(): boolean {
        let len = this.selectedKeys.length;
        return len > 0 && len < this.totalItems
    }

    public selectAllRows() {
        let params: any = this.defaultParams || {};
        if (this.baseUrl) {
            this.busy = true;
            // TODO: Spostare default params in instanza del componente generico
            Vue.axios.get(this.baseUrl + 'djvue/list_keys', {params: params}).then((response) => {
                this.selectedKeysDict = response.data.reduce(function (item: any, key: any) {
                    item[key] = true;
                    return item
                }, {});
            }).finally(() => {
                this.busy = false
            });
        }
    }

    public deselectAllRows() {
        this.selectedKeysDict = {};
    }

    private toggleAllRows(value: any) {
        if (this.allRowsSelected)
            this.deselectAllRows();
        else
            this.selectAllRows();
    }

    public getSelectedRows(): string[] {
        return this.selectedKeys;
    }
}
</script>

<style scoped>
.table-square-button {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
}

.buttons-table-cell > * {

}
</style>
