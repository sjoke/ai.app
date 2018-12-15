import React, { Component } from 'react';
import ReactEcharts from 'echarts-for-react';

import './pie.css';

class Pie extends Component {

    getOption = () =>{
        const option = 
            {
            title: {
                text: 'Top-5 accurracy',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            calculable: true,
            label: {
                formatter: function (params) {
                    return params.name + ', ' + (params.percent - 0).toFixed(0) + '%'
                }

            },
                series : [
                    {
                        name: 'rank-pie',
                        type: 'pie',
                        radius: [20, 100],
                        roseType: 'area',
                        data: [
                            { value: 0.6, name: 'banana' },
                            { value: 0.15, name: 'apple' },
                            { value: 0.1, name: 'pear' },
                            { value: 0.08, name: 'orange' },
                            { value: 0.07, name: 'peach' }

                        ]
                    }
                ]
        };

        return option;

    }

    render(){
        return (<ReactEcharts
            
            option={this.getOption()}
             />)
    }
}

export default Pie;