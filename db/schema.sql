CREATE DATABASE SpaceHub
GO

USE SpaceHub
GO

CREATE TABLE PlanoSubscricao (
    idPlanoSubscricao INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(50), 
    tipo NVARCHAR(20),
    preco_mensal DECIMAL(8,2),
    horas_salas_incl INT, 
    max_convidados INT
);
GO

CREATE TABLE Membro(
    idMembro INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100),    
    empresa NVARCHAR(100),
    NIF VARCHAR(9), 
    email NVARCHAR(150) UNIQUE,
    telemovel VARCHAR(20) NOT NULL,
    plano_id INT,
    data_inicio DATE,
    data_fim DATE,
    ativo BIT DEFAULT 1,
    CONSTRAINT UQ_Membro_email UNIQUE (email),
    CONSTRAINT FK_Membro_Plano FOREIGN KEY (plano_id) REFERENCES PlanoSubscricao(idPlanoSubscricao),
    CONSTRAINT CK_Membro_nif CHECK (LEN(nif) = 9 AND nif NOT LIKE '%[^0-9]%'),
    CONSTRAINT CK_Membro_datas CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);
GO

CREATE TABLE Posto(
    idPosto INT IDENTITY(1,1) PRIMARY KEY,
    numero INT,
    tipo VARCHAR(10), 
    ativo BIT, 
    descricao NVARCHAR(200) 
);
GO

CREATE TABLE Sala (
    idSala INT IDENTITY(1,1) PRIMARY KEY, 
    nome NVARCHAR(50), 
    capacidade INT, 
    equipamentos NVARCHAR(200), 
    preco_hora_extra DECIMAL(6,2)
);
GO

CREATE TABLE Reserva (
    idReserva INT IDENTITY(1,1) PRIMARY KEY, 
    data_Reserva DATE,
    hora_inicio TIME, 
    hora_fim TIME, 
    estado VARCHAR(15), 
    custo_calculado DECIMAL(8,2),
    membro_id INT NOT NULL,
    posto_id INT NOT NULL,
    sala_id INT NOT NULL,
    CONSTRAINT FK_Reserva_Membro FOREIGN KEY (membro_id) REFERENCES Membro(idMembro),
    CONSTRAINT FK_Reserva_Posto FOREIGN KEY (posto_id) REFERENCES Posto(idPosto),
    CONSTRAINT FK_Reserva_Sala FOREIGN KEY (sala_id) REFERENCES Sala(idSala)
);
GO

-- 3. Criar Fatura antes de ServicoExtra (porque ServicoExtra depende de Fatura)
CREATE TABLE Fatura (
    idFatura INT IDENTITY(1,1) PRIMARY KEY,
    membro_id INT NOT NULL,
    valor_base DECIMAL(8,2),
    valor_extras DECIMAL(8,2),
    pago BIT,
    data_emissao DATE,
    data_vencimento DATE,
    data_pagamento DATE,
    CONSTRAINT FK_Fatura_Membro FOREIGN KEY (membro_id) REFERENCES Membro(idMembro)
);
GO

-- 4. Agora já podemos criar ServicoExtra
CREATE TABLE ServicoExtra (
    idServicoExtra INT IDENTITY(1,1) PRIMARY KEY,
    membro_id INT NOT NULL, 
    fatura_id INT NOT NULL,
    tipo VARCHAR(20),
    data_servico DATE,
    quantidade INT,
    custo_unit DECIMAL(6,2),
    CONSTRAINT FK_ServicoExtra_Membro FOREIGN KEY (membro_id) REFERENCES Membro(idMembro),
    CONSTRAINT FK_ServicoExtra_Fatura FOREIGN KEY (fatura_id) REFERENCES Fatura(idFatura)
);
GO

CREATE TABLE Visitante (
    idVisitante INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100),
    empresa NVARCHAR(100) NOT NULL,
    data_visita DATE,
    hora_entrada TIME,
    hora_saida TIME NOT NULL,
    membro_id INT,
    CONSTRAINT FK_Visitante_Membro FOREIGN KEY (membro_id) REFERENCES Membro(idMembro)
);
GO

CREATE TABLE Utilizador (
    idUtilizador INT IDENTITY(1,1) PRIMARY KEY,
    membro_id INT,
    login_utilizador VARCHAR(50),
    password_hash VARCHAR(255),
    perfil VARCHAR(10),
    ativo BIT,
    CONSTRAINT FK_Utilizador_Membro FOREIGN KEY (membro_id) REFERENCES Membro(idMembro)
);
GO