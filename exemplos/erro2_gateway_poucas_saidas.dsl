processo {
    nome = "Erro 2: Gateway com Poucas Saídas";
    dono = "Departamento de Testes";
    inicio = ativ1;

    atividades {
        ativ1 {
            nome = "Atividade Inicial";
            tipo = "tarefa";
            responsavel = "Funcionário";
            tempo = 1;
            custo = 0;
            seguinte = { gateway_problema };
        }

        gateway_problema {
            nome = "Gateway com Apenas 1 Saída";
            tipo = "gateway";
            responsavel = "Sistema";
            seguinte = { ativ2 };
        }

        ativ2 {
            nome = "Atividade 2";
            tipo = "tarefa";
            responsavel = "Funcionário";
            seguinte = { fim };
        }
    }

    fim = "Processo Encerrado";
}
