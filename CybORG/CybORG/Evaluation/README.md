# Recorded Results

<table style="width: 150%">
    <thead>
        <tr>
            <th colspan="1" rowspan="3"></th>
        </tr>
        <tr>
            <th colspan="3">30 steps</th>
            <th colspan="3">50 steps</th>
            <th colspan="3">100 steps</th>
        </tr>
        <tr>
            <th>B-line</th>
            <th>Meander</th>
            <th>Sleep</th>
            <th>B-line</th>
            <th>Meander</th>
            <th>Sleep</th>
            <th>B-line</th>
            <th>Meander</th>
            <th>Sleep</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Tuned PPO (130)</th>
        </tr>
        <tr>
            <td>B-Line (100)</td>
            <td>-11.12 ± 3.22</td>
            <td>-12.59 ± 3.13</td>
            <td>-1.09 ± 0.99</td>
            <td>-18.63 ± 6.17</td>
            <td>-31.99 ± 7.67</td>
            <td>-1.74 ± 1.31</td>
            <td>-40.25 ± 23.19</td>
            <td>-88.95 ± 17.05</td>
            <td>-3.71 ± 1.92</td>
        </tr>
        <tr>
            <th>Vanilla PPO</th>
        </tr>
        <tr>
            <td>B-Line (100)</td>
            <td>-14.13 ± 3.90</td>
            <td>-12.37 ± 3.68</td>
            <td>-2.48 ± 1.44</td>
            <td>-25.12 ± 6.09</td>
            <td>-30.47 ± 14.48</td>
            <td>-3.94 ± 1.89</td>
            <td>-55.45 ± 14.59</td>
            <td>-87.58 ± 52.46</td>
            <td>-7.52 ± 2.85</td>
        </tr>
        <tr>
            <td>Meander (100)</td>
            <td>-56.83 ± 11.61</td>
            <td>-25.98 ± 10.65</td>
            <td>-2.61 ± 1.37</td>
            <td>-115.27 ± 15.17</td>
            <td>-83.57 ± 34.65</td>
            <td>-4.01 ± 1.91</td>
            <td>-256.48 ± 33.60</td>
            <td>-253.61 ± 101.03</td>
            <td>-8.64 ± 2.30</td>
        </tr>
    </tbody>
    <tbody>
        <tr>
            <th>Vanilla DQN</th>
        </tr>
        <tr>
            <td>B-Line (100)</td>
            <td>-17.66 ± 9.14</td>
            <td>-13.88 ± 5.75</td>
            <td>-0.32 ± 0.51</td>
            <td>-34.97 ± 19.34</td>
            <td>-38.80 ± 18.22</td>
            <td>-0.62 ± 0.78</td>
            <td>-88.69 ± 44.49</td>
            <td>-141.73 ± 49.82</td>
            <td>-1.31 ± 1.03</td>
        </tr>
        <tr>
            <td>Meander (100)</td>
            <td>-27.42 ± 16.38</td>
            <td>-13.70 ± 10.02</td>
            <td>-0.34 ± 0.55</td>
            <td>-65.13 ± 28.11</td>
            <td>-48.71 ± 28.17</td>
            <td>-0.6 ± 0.73</td>
            <td>-169.93 ± 44.76</td>
            <td>-179.77 ± 69.18</td>
            <td>-1.28 ± 1.24</td>
        </tr>
    </tbody>
    <tbody>
        <tr>
            <th>Vanilla A2C</th>
        </tr>
        <tr>
            <td>B-Line (100)</td>
            <td>-60.07 ± 5.90</td>
            <td>-29.85 ± 9.45</td>
            <td>-0.08 ± 0.27</td>
            <td>-120.86 ± 8.65</td>
            <td>-106.50 ± 26.56</td>
            <td>-0.13 ± 0.34</td>
            <td>-273.78 ± 11.96</td>
            <td>-301.86 ± 81.84</td>
            <td>-0.15 ± 0.39</td>
        </tr>
        <tr>
            <td>Meander (100)</td>
            <td>-33.11 ± 7.64</td>
            <td>-20.77 ± 6.66</td>
            <td>-6.88 ± 2.29</td>
            <td>-59.34 ± 11.18</td>
            <td>-34.98 ± 14.30</td>
            <td>-11.83 ± 3.07</td>
            <td>-121.39 ± 15.37</td>
            <td>-63.42 ± 25.49</td>
            <td>-22.48 ± 4.13</td>
        </tr>
    </tbody>
</table>
