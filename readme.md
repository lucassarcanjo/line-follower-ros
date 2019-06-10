# ROS Line Follower

Teste com remap dos valores lidos pelos sensores esquerdo e direito a fim de garantir estabilidade dos dois sensores no momento de obter o erro unificado:

erro = light_l - light_r

O remap consiste em pegar os valores obtidos de cada sensor e convertê-los da escala máximo-mínimo preto-branco previamente medidos individualmente para a escala 0-100 onde o valor de threshold é 50.

Possibilidade de implementação posterior: 
- compensação do sensor através de um valor somado à leitura, como um coeficiente b numa função linear
- salvar os valores de calibração num arquivo txt para evitar calibrações em toda inicialização

