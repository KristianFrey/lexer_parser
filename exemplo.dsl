processo {
    nome = "Processo de Compra";
    dono = "Departamento Financeiro";
    inicio = solicitar_compra;

    atividades {

        solicitar_compra {
            nome = "Solicitar Compra";
            tipo = "tarefa";
            responsavel = "Funcionário";
            tempo = 2;
            custo = 0;
            seguinte = { avaliar_compra };
        }

        avaliar_compra {
            nome = "Avaliar Compra";
            tipo = "gateway";
            responsavel = "Gerente";
            seguinte = {
                aprovado -> aprovar_compra,
                rejeitado -> fim
            };
        }

        aprovar_compra {
            nome = "Aprovar Compra";
            tipo = "tarefa";
            responsavel = "Diretor";
            tempo = 1;
            custo = 500;
            seguinte = { fim };
        }
    }

    fim = "Processo Encerrado";
}
