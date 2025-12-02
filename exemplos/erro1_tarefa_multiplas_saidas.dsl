processo {
    nome = "Erro 1: Tarefa com Múltiplas Saídas";
    dono = "Departamento de Testes";
    inicio = tarefa_problema;

    atividades {
        tarefa_problema {
            nome = "Tarefa com Erro de Cardinalidade";
            tipo = "tarefa";
            responsavel = "Funcionário";
            tempo = 1;
            custo = 0;
            seguinte = { opcao1 -> ativ2, opcao2 -> ativ3 };
        }

        ativ2 {
            nome = "Atividade 2";
            tipo = "tarefa";
            responsavel = "Funcionário";
            seguinte = { fim };
        }

        ativ3 {
            nome = "Atividade 3";
            tipo = "tarefa";
            responsavel = "Funcionário";
            seguinte = { fim };
        }
    }

    fim = "Processo Encerrado";
}
